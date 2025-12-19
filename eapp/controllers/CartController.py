from flask import app, jsonify, render_template, request
from sklearn.gaussian_process.kernels import Product

from eapp.dao import CartDao
from flask_login import login_required, current_user
from eapp.dao import ProductDao
from eapp.models import Product
from eapp.models.Invoice import InvoiceStatusEnum
from eapp.models.Payment import PaymentStatus

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
    return render_template('page/cart_component_item.html', list_prod=cart_item)

def load_my_cart():
    user_id = current_user.id
    # Lấy sản phẩm trong giỏ hàng
    cart_item = CartDao.get_cart_by_userId_dao(user_id)
    # Lấy đơn hàng
    tab = request.args.get("tab", "order_all")
    invoice_status = None
    payment_status = None

    if tab == "pending_payment":
        payment_status = PaymentStatus.pending

    elif tab == "pending_processing":
        invoice_status = InvoiceStatusEnum.PENDING
        payment_status = PaymentStatus.success

    elif tab == "completed":
        invoice_status = InvoiceStatusEnum.COMPLETED
        payment_status = PaymentStatus.success

    elif tab == "cancelled":
        invoice_status = InvoiceStatusEnum.CANCELLED

    list_prod = ProductDao.get_product_by_status_dao(
        user_id=current_user.id,
        invoice_status=invoice_status,
        payment_status=payment_status
    )
    print("list_prod_id", list_prod)
    return render_template("page/cart.html", tab=tab, list_pro=cart_item, list_order=list_prod)