
from operator import ge
from flask import json, jsonify, render_template, request, session

from eapp.dao import CategoryDao, ProductDao
from flask import render_template, request



def load_staff():
    category = CategoryDao.list()
    dishes = ProductDao.list()
    return render_template('/staff/staff.html', category=category,dishes=dishes)


def addToOrder():
    """
        id:
            id
            name
            price
            quantity
    """
    order = session.get('order',{})
    data = request.json
    id = str(data.get('id'))
    is_change_quantity = False

    if id in order:
        order[id]['quantity'] += 1
        is_change_quantity = True
    else:
        order[id] = {
            "id": id,
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": 1
        }

    session['order'] = order

 
    return jsonify({
        "succes" : True,
        "item" : order[id],
        "total_quantity" : sum(i['quantity'] for i in order.values()),
        "is_change_quantity" : is_change_quantity
    })
    

def create_invoice():
    order = session.get('order',{})

    session.pop('order',None)
    return jsonify({
        "success" : True
    })


from flask import render_template, request, redirect



def warehouse_page():

    warehouses = [
        {'id': 1, 'name': 'Kho Tổng'},
        {'id': 2, 'name': 'Kho Quầy'}
    ]
    ingredients = [
        {'id': 1, 'name': 'Cafe hạt', 'unit': 'kg'},
        {'id': 2, 'name': 'Sữa tươi', 'unit': 'lít'},
        {'id': 3, 'name': 'Đường', 'unit': 'kg'}
    ]

    return render_template('admin/warehouse.html',
                           warehouses=warehouses,
                           ingredients=ingredients)


def create_ticket():
    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type')
        ingr_id = request.form.get('ingredient_id')
        qty = request.form.get('quantity')

        print(f"Xử lý phiếu {ticket_type} cho món {ingr_id} số lượng {qty}")

        return redirect('/admin/warehouse')