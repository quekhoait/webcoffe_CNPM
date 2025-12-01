
from operator import ge
from flask import json, jsonify, render_template, request, session

from eapp.dao import CategoryDao, ProductDao, RuleDAO
from eapp.models.Rule import RuleType




def load_staff():
    category = CategoryDao.list()
    dishes = ProductDao.list()
    order = session.get('order', {})
    rules = RuleDAO.list({'rule_type': RuleType.SERVICE})
    total_price_tmp = sum(item['quantity'] * item['price'] for item in order.values())
    total_price = total_price_tmp + calulate_service_fee(total_price_tmp)
    return render_template('/staff/staff.html', category=category, dishes=dishes, total_price=total_price,total_price_tmp=total_price_tmp,rules=rules)


def addToOrder():
    """
        id:
            id
            name
            price
            bonus_quantity
            is_set_quantity
    """
    order = session.get('order',{})
    data = request.json
    id = str(data.get('id'))
    # is_change_quantity = False
    bonus_quantity = int(data.get('bonus_quantity',1))
    
    if id in order and data.get('is_set_quantity'):
        order[id]['quantity'] = bonus_quantity
    elif id in order:
        order[id]['quantity'] += bonus_quantity
        # is_change_quantity = True
        print("OKK bro")

    else:
        order[id] = {
            "id": id,
            "name": data.get('name'),
            "price": data.get('price'),
            "quantity": bonus_quantity
        }

    session['order'] = order

    item_html = render_template('staff/order_item.html',dish=order[id])
    total_price_tmp = sum(item['quantity']*item['price'] for item in order.values())
    total_price = total_price_tmp + calulate_service_fee(total_price_tmp)
    return jsonify({
        "succes" : True,
        "item_html" : item_html,
        # "total_quantity" : sum(i['quantity'] for i in order.values()),
        "total_price" : total_price,
        'item' : order[id],
        'total_price_tmp' : total_price_tmp
        # "is_change_quantity" : is_change_quantity
    })
    
def calulate_service_fee(total_price):
    rules = RuleDAO.list({'rule_type': RuleType.SERVICE})
    service_fee = 0
    for rule in rules:
        if rule.unit == "%":
            service_fee += total_price * (rule.value / 100)
        else:
            service_fee += rule.value
    return service_fee

def create_invoice():
    order = session.get('order',{})

    session.pop('order',None)
    return jsonify({
        "success" : True
    })