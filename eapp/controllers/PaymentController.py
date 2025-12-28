from unittest import result
from flask import app, jsonify, render_template, request, session
from flask_login import  current_user, login_required
from datetime import datetime
from eapp.dao import ProductDao, PaymentDao
from eapp.models.Payment import PaymentStatus
from eapp.Momo import momo
from eapp.services.RuleService import RuleService
from flask import render_template, request, session, redirect
from flask_login import current_user, login_required
from eapp.dao import ProductDao
from eapp import db
from eapp.services.inventory.InventoryValidator import InventoryValidator
from eapp.services.inventory.StockService import StockService
from eapp.controllers import index
from eapp.models import Invoice
from flask_login import login_required

# @login_required
def load_data():
    if request.method == "POST":
        invoice_items = session["checkout_items"] = request.json
        insufficient_products, remain_stock = InventoryValidator.get_insufficient_products(invoice_items, 1)
        if len(insufficient_products) >0 :
            return jsonify({
                "status": "error",
                "message": "Không thể cung cấp đủ",
                "products": insufficient_products
            })
        return jsonify({
            "status": "success"
        })
    items = session.get("checkout_items")
    if not items:
        return redirect("/cart")

    products = []
    total = 0
    for item in items:
        prod = ProductDao.get_by_id(item["product_id"])
        qty = int(item["quantity"])
        total_item = prod.price * qty
        products.append({
            "image": prod.image,
            "name": prod.name,
            "price": prod.price,
            "qty": qty,
            "total": total_item
        })

        total += total_item
    extra_fee = RuleService.calulate_service_fee(total)
    final_total = total + extra_fee
    return render_template(
        "page/checkout.html",
        user_info=current_user,
        products=products,
        total = final_total,
    )


"""
    [{}]
        product_id
        quantity
        price
"""
def created_payment():
    data = request.get_json()
    note = data.get("note")
    payment_method = data.get("payment_method")
    cart_items = session.get("checkout_items")
    if not cart_items:
        return jsonify({"status": "error", "message": "Giỏ hàng trống"})

    if not current_user.address or not current_user.phone or not current_user.name:
        return jsonify({
            "status": "error",
            "message": "Vui lòng cập nhật thông tin trước khi đặt hàng!"
        })
    sub_total = 0
    for item in cart_items:
        prod = ProductDao.get_by_id(item["product_id"])
        sub_total += prod.price * int(item["quantity"])
    extra_total = RuleService.calulate_service_fee(sub_total)
    invoice = PaymentDao.create_Invoice_dao(
        user_id=current_user.id,
        subtotal=sub_total,
        extra_fee_total=extra_total,
        payment_method=payment_method,
        note=note
    )

    for item in cart_items:
        prod=ProductDao.get_by_id(item["product_id"])
        PaymentDao.create_InvoiceDetail_dao(prod.id, invoice.id, int(item["quantity"]),prod.price)

    StockService.reserve_stock_for_invoice(
        invoice=invoice,
        warehouse_id=index.get_current_warehouse()
    )
    momo_order_id = f"{invoice.order_code}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    payment=PaymentDao.create_Payment_dao(
        invoice_id=invoice.id,
        amount=sub_total+extra_total,
    )
    momo_res = momo.created_pay(momo_order_id, sub_total+extra_total)
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


def repay_payment():
    invoice_id = request.get_json().get("invoice_id")
    result = PaymentDao.repay_payment_dao(
        invoice_id=invoice_id,
    )
    if result.momo_id and result.payUrl:
        return jsonify({
            "status": "success",
            "pay_url": result.payUrl
        })
    invoice = Invoice.query.get(invoice_id)

    momo_order_id = f"{invoice.order_code}_{int(datetime.now().timestamp())}"

    momo_res = momo.created_pay(momo_order_id, result.amount)

    if momo_res.get("resultCode") != 0:
        result.status = PaymentStatus.failed
        db.session.commit()
        return jsonify({
            "status": "error",
            "message": momo_res.get("message", "Lỗi hệ thống")
        })

    result.momo_id = momo_order_id
    result.payUrl = momo_res["payUrl"]
    db.session.commit()
    return jsonify({
        "status": "success",
        "pay_url": result.payUrl
    })