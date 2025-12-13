
from operator import ge
from flask import json, jsonify, render_template, request, session

from eapp.dao import CategoryDao, ProductDao, RuleDAO
from eapp.models.Invoice import Invoice
from eapp.models.Rule import RuleType
from eapp.services.InvoiceService import InvoiceService


def load_staff():
    category = CategoryDao.list()
    products = ProductDao.list()
    invoice = session.get('invoice', {})
    rules = RuleDAO.list({'rule_type': RuleType.SERVICE})
    total_price_tmp = InvoiceService.calculate_total(invoice)
    total_price = InvoiceService.calculate_final_total(total_price_tmp)

    return render_template('/staff/staff.html',
                           category=category, 
                           products=products, 
                           total_price=total_price,
                           total_price_tmp=total_price_tmp,
                           rules=rules)


"""
invoice
    id:
        id *product
        name
        price
        bonus_quantity
        is_set_quantity
"""
def addItemToInvoice():
    invoice = session.get('invoice',{})
    id = str(request.json.get('id'))
    data = request.json
    InvoiceService.add_item_to_invoice(invoice,data)
    session['invoice'] = invoice
    total = InvoiceService.calculate_total(invoice)

    return jsonify({
        "success" : True,
        "item_html" : render_template('staff/invoice_item.html',invoice_item=invoice[id]),
        "total_price" : InvoiceService.calculate_final_total(total),
        'item' : invoice[id],
        'total_price_tmp' : total,
    })
    
"""
    id
"""
def removeItemFromInvoice():
    invoice = session.get('invoice')
    item_id = str(request.json.get('id'))

    InvoiceService.remove_item_from_invoice(invoice,item_id)
    session['invoice'] = invoice
    total_price_tmp = InvoiceService.calculate_total(invoice)
    total_price = InvoiceService.calculate_final_total(total_price_tmp)
    
    return jsonify({
        "success" : True,
        "total_price" : total_price,
        "total_price_tmp" : total_price_tmp
    })
 



def create_invoice():
    invoice_items = session.get('invoice',{})
    # tạm thời test với staff_id = 1 request.json.get('staff_id')
    invoice_data = {
        'staff_id' : request.json.get('staff_id'),
        'invoice_items' : invoice_items
    }

    InvoiceService.create_invoice(invoice_data)

    session.pop('invoice',None)

    return jsonify({
        "success" : True
    })

def clear_invoice():
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