
from operator import ge
from flask import json, jsonify, render_template, request, session
from flask_login import current_user
from eapp.index import socketio
from eapp.dao import CategoryDao, ProductDao, RuleDAO
from eapp.models.Invoice import Invoice, PaymentMethod
from eapp.models.Rule import RuleType
from eapp.services.InventoryService import InventoryService
from eapp.services.InvoiceService import InvoiceService


def load_staff():
    user = current_user
    category = CategoryDao.list()
    products = ProductDao.list()
    invoice = session.get('invoice', {})
    rules = RuleDAO.list({'rule_type': RuleType.SERVICE})
    total_price_tmp = InvoiceService.calculate_total(list(invoice.values()))
    total_price = InvoiceService.calculate_final_total(total_price_tmp)
    status_map = InventoryService.get_product_makeable_map(products=products,warehouse_id=session.get('warehouse_id',1))
    return render_template('/staff/staff.html',
                           category=category, 
                           products=products, 
                           total_price=total_price,
                           total_price_tmp=total_price_tmp,
                           rules=rules,
                           user=user,
                           warehouse_id=session.get('warehouse_id',1),
                           product_status_map=status_map)


"""
invoice
    id:
        id *product
        name
        price
        bonus_quantity
        is_set_quantity

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
    
    new_quantity = InvoiceService.calculate_new_quantity(invoice,data)
    
    #Kiểm tra kho đáp ứng được món này ko
    makeable_product = InventoryService.get_quantity_product_makeable(
        product_id=data['id'],
        quantity=new_quantity,
        warehouse_id=session.get('warehouse_id',1)
    )

    if makeable_product['ingredient_insufficient']:
        return jsonify({
            "success": False,
            "message": "Nguyên liệu không đáp ứng đủ cho số lượng hiện tại",
            "ingredient_insufficient": makeable_product['ingredient_insufficient'],
            "makeable_quantity": makeable_product['makeable_quantity'],
            "item": invoice[product_id],
            "total_price": None
        })

    InvoiceService.add_item_to_invoice(invoice,data,new_quantity)

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
 



def create_invoice():
    invoice_items = session.get('invoice',{})

    invoice_data = {
        'staff_id' : current_user.id,
        'invoice_items' : list(invoice_items.values()),
        'payment_method' : PaymentMethod.CASH,
    }

    invoice = InvoiceService.create_invoice(invoice_data)

    session.pop('invoice',None)


    
    # --- PUSH SỰ KIỆN QUA SOCKETIO ---
    # Phát sự kiện 'new_invoice' tới tất cả client đang quan tâm
    return jsonify({
        "success" : True
    })

def clear_invoice():
    socketio.emit('receive', {'msg':"Dit me ao that day"})

    session.pop('invoice')
    return jsonify({
        "success" : True
    })


from flask import render_template, request, redirect


def create_ticket():
    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type')
        ingr_id = request.form.get('ingredient_id')
        qty = request.form.get('quantity')

        print(f"Xử lý phiếu {ticket_type} cho món {ingr_id} số lượng {qty}")

        return redirect('/admin/warehouse')