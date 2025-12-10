from flask import app, jsonify, render_template, request
from eapp.dao.CartDetailDao import created_cart_detail_dao
from flask_login import login_required, current_user

def created_cart_detail():
    cart_id = 2
    if not cart_id:
        return jsonify({"error": "Khong tồn tại cart"}), 400
    cart = created_cart_detail_dao(cart_id)
    if not cart:
        return jsonify({"error": "Failed"}), 500
    return jsonify({
        "message": "success",
        "cart": {
            "id": cart.id,
            "user_id": cart.user_id
        }
    }), 200