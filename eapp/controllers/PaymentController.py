from flask import app, jsonify, render_template, request, session
from flask_login import  current_user, login_required

from eapp.dao import ProductDao, PaymentDao

from flask import render_template, request, session, redirect
from flask_login import current_user, login_required
from eapp.dao import ProductDao



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


def created_payment():
    # payment_method = request.form.get("payment_method")
    payment_method="MOMO"
    cart_items = session.get("checkout_items")
    print(cart_items)
    if not cart_items:
        return jsonify({"status": "error", "message": "Giỏ hàng trống"})

    if not current_user.address or not current_user.phone or not current_user.name:
        return jsonify({
            "status": "error",
            "message": "Vui lòng cập nhật thông tin trước khi đặt hàng!"
        })
    total = 0
    for item in cart_items:
        prod = ProductDao.get_by_id(item["product_id"])
        total += prod.price * int(item["quantity"])

    invoice = PaymentDao.create_Invoice_dao(
        user_id=current_user.id,
        total=total,
        payment_method=payment_method,
        note="coi nha"
    )
    print("invoice: ", invoice)
    # for item in cart_items:
    #     prod=ProductDao.get_by_id(item["product_id"])
    #     PaymentDao.create_InvoiceDetail_dao(prod.id, invoice.id, int(item["quantity"]), prod.price)
    #
    # PaymentDao.create_Payment_dao(
    #     invoice_id=invoice.id,
    #     amount=total,
    #     payment_method=payment_method,
    #     status="pending"  # chờ thanh toán
    # )
    return jsonify({
        "status": "success",
        "invoice_id": invoice.id,
        "total": total
    })

