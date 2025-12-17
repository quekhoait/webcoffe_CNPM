from flask import app, jsonify, render_template, request, session
from flask_login import  current_user, login_required
from datetime import datetime
from eapp.dao import ProductDao, PaymentDao
from eapp.models.Payment import PaymentStatus
from eapp.Momo import momo

from flask import render_template, request, session, redirect
from flask_login import current_user, login_required
from eapp.dao import ProductDao
from eapp import db



def load_data():
    if request.method == "POST":
        session["checkout_items"] = request.json

    items = session.get("checkout_items")
    if not items:
        return redirect("/cart")
    products = []
    total = 0
    for item in items:
        prod = ProductDao.get_by_id(item["product_id"])
        qty = int(item["quantity"])
        cost = prod.price * qty

        products.append({
            "image": prod.image,
            "name": prod.name,
            "price": prod.price,
            "qty": qty,
            "cost": cost
        })

        total += cost
    return render_template(
        "page/checkout.html",
        user_info=current_user,
        products=products,
        total=total
    )


"""
    [{}]
        product_id
        quantity
        price
"""
def created_payment():
    # payment_method = request.form.get("payment_method")
    payment_method="MOMO"
    cart_items = session.get("checkout_items")
    if not cart_items:
        return jsonify({"status": "error", "message": "Giỏ hàng trống"})

    if not current_user.address or not current_user.phone or not current_user.name:
        return jsonify({
            "status": "error",
            "message": "Vui lòng cập nhật thông tin trước khi đặt hàng!"
        })
    total = 0
    for item in cart_items:
        # prod = ProductDao.get_by_id(item["product_id"])
        total += float(item["price"]) * int(item["quantity"])
    invoice = PaymentDao.create_Invoice_dao(
        user_id=current_user.id,
        total=total,
        payment_method=payment_method,
        note="coi nha"
    )
    for item in cart_items:
        prod=ProductDao.get_by_id(item["product_id"])
        PaymentDao.create_InvoiceDetail_dao(prod.id, invoice.id, int(item["quantity"]), float(item["price"]))

    momo_order_id = f"{invoice.order_code}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    payment=PaymentDao.create_Payment_dao(
        invoice_id=invoice.id,
        amount=total,
    )
    momo_res = momo.created_pay(momo_order_id, total)
    if momo_res.get("resultCode") != 0:
        payment.status = PaymentStatus.failed
        db.session.commit()
        return jsonify({
            "status": "error",
            "message": momo_res.get("message", "Thanh toán MoMo thất bại"),
            "momo_response": momo_res  # debug
        })
    payment.momo_id = momo_order_id
    payment.payUrl = momo_res["payUrl"]
    db.session.commit()

    return jsonify({
        "status": "success",
        "pay_url": payment.payUrl
    })



