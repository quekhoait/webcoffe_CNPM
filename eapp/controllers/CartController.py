from flask import app, jsonify, render_template, request
from eapp.dao import CartDao
from flask_login import login_required, current_user

# Theem sanr pham vao cart
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")
    quantity=data.get("quantity")
    user_id=current_user.id

    product= CartDao.add_to_cart_dao(product_id, user_id, quantity)
    print(product)
    return jsonify({
        "status": "success",
        "message":"Đã thêm thành công",
        "data":  product.to_dict()
        })

def get_cart_by_userId():
    user_id=current_user.id
    cart_item=CartDao.get_cart_by_userId_dao(user_id)
    print([item.to_dict() for item in cart_item])
    return render_template('page/cart_component_item.html', list_prod=cart_item)