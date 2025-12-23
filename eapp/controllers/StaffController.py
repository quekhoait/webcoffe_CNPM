
from operator import ge
from flask import json, jsonify, render_template, request, session
from flask_login import current_user
from eapp.dao import CategoryDao, ProductDao, RuleDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Invoice import Invoice, PaymentMethod
from eapp.models.Rule import RuleType
from eapp.services.InvoiceService import InvoiceService
from eapp.services.inventory.InventoryValidator import InventoryValidator
from eapp.services.inventory.RecipeService import RecipeService


def load_staff():
    # if 'available_stock_tmp' not in session:
    #     session['available_stock_tmp'] = WarehouseDAO.get_available_stock_map(get_current_warehouse())
    user = current_user
    category = CategoryDao.list()
    products = ProductDao.list()
    invoice = session.get('invoice', {})
    rules = RuleDAO.list(RuleDAO.RuleFilter(rule_type=RuleType.SERVICE))
    total_price_tmp = InvoiceService.calculate_total(list(invoice.values()))
    total_price = InvoiceService.calculate_final_total(total_price_tmp)
    status_map = InventoryValidator.get_product_makeable_map(products=products,warehouse_id=session.get('warehouse_id',1))
    return render_template('/staff/staff.html',
                           category=category, 
                           products=products, 
                           total_price=total_price,
                           total_price_tmp=total_price_tmp,
                           rules=rules,
                           user=user,
                           warehouse_id=session.get('warehouse_id',1),
                           product_status_map=status_map)



def render_invoice_item():
    return render_template('/staff/invoice_item.html')

"""

invoice:
    {
        'product_id' : {
            product_id,
            name,
            price,
            quantity
        }
    }

data 
    "id": id,
    "name": name,
    "price": price,
    "bonus_quantity": bonusQuantity,
    "is_set_quantity": setQuantity
"""
def addItemToInvoice():
    invoice = session.get('invoice', {})
    data = request.json
    product_id = str(data.get('id'))
    quantity = data.get('quantity', 1)
    bonus_quantity = int(data.get('bonus_quantity', 1))
    
    message = InvoiceService.is_invalid_value(invoice.get(product_id, {}).get('quantity', 0),bonus_quantity,data.get('is_set_quantity'))

    #kiểm tra dữ liệu vào có hợp lệ ko
    if message:
        return jsonify({
            "success": False,
            "message": message,
            "ingredient_insufficient": [],
            "makeable_quantity": 0,
            "item": None,
            "total_price": None
        })


    # nếu là nhập liệu thì gỡ tạm để reset món đó về 0
    item_tmp = None
    if data['is_set_quantity']:
        item_tmp = invoice.pop(product_id,None)
    required_ingredient_map = RecipeService.get_required_ingredient_map_from_session_invoice(invoice.values())
    
    # 10 
    
    available_stock = {
        key : max(0, value - required_ingredient_map.get(key, 0))
        for key, value in WarehouseDAO.get_available_stock_map(get_current_warehouse()).items()     
    }
    
    # print(required_ingredient_map)
    # print(available_stock)
    # print(WarehouseDAO.get_available_stock_map(get_current_warehouse()))

    #Kiểm tra kho đáp ứng được món này ko
    makeable_product = InventoryValidator.get_quantity_product_makeable(
        product_id=data['id'],
        quantity=int(data['bonus_quantity']),
        available_stock_map = available_stock
    )

    # print(makeable_product)
    # print(invoice)
    
    

    if makeable_product['ingredient_insufficient']:
        return jsonify({
            "success": False,
            "message": "Nguyên liệu không đáp ứng đủ cho số lượng hiện tại",
            "ingredient_insufficient": makeable_product['ingredient_insufficient'],
            "makeable_quantity": makeable_product['makeable_quantity'],
            "item": invoice.get(product_id,item_tmp),
            "total_price": None
        })
    

    # check ok rồi thì thêm lại
    if data['is_set_quantity']:
        invoice[product_id] = item_tmp

    InvoiceService.add_item_to_invoice(invoice,data,InvoiceService.calculate_new_quantity(invoice,data))

    session['invoice'] = invoice
    total = InvoiceService.calculate_total(list(invoice.values()))

    return jsonify({
        "success": True,
        "message": "Thêm món thành công",
        "item": invoice[product_id],
        "item_html": render_template('staff/invoice_item.html', invoice_item=invoice[product_id]),
        "total_price": InvoiceService.calculate_final_total(total),
        "total_price_tmp": total,
        "ingredient_insufficient": [],
        "makeable_quantity": quantity
    })
    
"""
    id
"""
def removeItemFromInvoice():
    invoice = session.get('invoice')
    item_id = str(request.json.get('id'))

    InvoiceService.remove_item_from_invoice(invoice,item_id)
    session['invoice'] = invoice
    total_price_tmp = InvoiceService.calculate_total(list(invoice.values()))
    total_price = InvoiceService.calculate_final_total(total_price_tmp)
    
    return jsonify({
        "success" : True,
        "total_price" : total_price,
        "total_price_tmp" : total_price_tmp
    })
 

"""
    invoice:
        {
            'product_id' : {
                product_id,
                name,
                price,
                quantity
            }
        }
"""

def create_invoice():
    invoice_items = session.get('invoice',{})

    invoice_data = {
        'staff_id' : current_user.id,
        'invoice_items' : list(invoice_items.values()),
        'payment_method' : PaymentMethod.CASH,
    }
    #kiểm tra tồn kho lần nữa thì kết thúc hàm trả thông báo lỗi
    check_result, available_stock_map = InventoryValidator.get_insufficient_products(invoice_items.values(),get_current_warehouse())

    if check_result:
        return jsonify({
            'success' : False,
            'insufficient_products' : check_result
        })

    
    used_stock_map = {
        key: value - available_stock_map[key]
        for key,value in WarehouseDAO.get_available_stock_map(get_current_warehouse()).items()
    }
    

    #tạo hóa đơn pending
    invoice = InvoiceService.create_invoice(invoice_data,get_current_warehouse(),used_stock_map)

    #cập nhật reserved trên kho lần nữa thì kết thúc hàm trả thông báo lỗi

    session.pop('invoice',None)

    return jsonify({
        "success" : True
    })

def clear_invoice():

    session.pop('invoice')
    return jsonify({
        "success" : True
    })


def get_current_warehouse():
    return 1

from flask import render_template, request, redirect


def create_ticket():
    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type')
        ingr_id = request.form.get('ingredient_id')
        qty = request.form.get('quantity')

        print(f"Xử lý phiếu {ticket_type} cho món {ingr_id} số lượng {qty}")

        return redirect('/admin/warehouse')