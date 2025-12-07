from flask import app, jsonify, render_template, request
from eapp.dao.CartDao import created_cart_dao
from flask_login import login_required, current_user

def created_cart():
    user_id = 2
    if not user_id:
        return jsonify({"error": "Khong có user"}), 400
    # Lấy cart cũ hoặc tạo cart mới
    cart = created_cart_dao(user_id)
    if not cart:
        return jsonify({"error": "Failed"}), 500
    return jsonify({
        "message": "success",
        "cart": {
            "id": cart.id,
            "user_id": cart.user_id
        }
    }), 200
