
from operator import ge
from flask import json, jsonify, render_template, request, session

from eapp.dao import CategoryDao, ProductDao




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