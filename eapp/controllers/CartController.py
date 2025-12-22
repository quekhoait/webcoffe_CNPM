from flask import app, jsonify, render_template, request, session
# from sklearn.gaussian_process.kernels import Product

from eapp.dao import CartDao
from eapp.services import  RuleService
from flask_login import login_required, current_user
from eapp.dao import ProductDao
from eapp.models import Product
from eapp.models.Invoice import InvoiceStatusEnum
from eapp.models.Payment import PaymentStatus
from eapp.services.inventory.InventoryValidator import InventoryValidator

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
    user_id = current_user.id
    cart_items = CartDao.get_cart_by_userId_dao(user_id)
    warehouse_id = session.get('warehouse_id', 1)
    # Lấy tồn kho 1 lần
    available_stock_map = InventoryValidator.get_product_makeable_map(cart_items,session.get('warehouse_id',1))
    list_prod_status = {}
    for cart in cart_items:
        product_id = cart.product.id
        quantity = cart.quantity
        check = InventoryValidator.get_quantity_product_makeable(
            product_id,
            quantity,
            available_stock_map
        )
        print(check["makeable_quantity"])
        list_prod_status[product_id] = {
            "in_stock": check["makeable_quantity"] >= quantity,
            "makeable_quantity": check["makeable_quantity"]
        }
    print(cart_items)
    print(list_prod_status)
    return render_template(
        'page/cart_component_item.html',
        list_prod=cart_items,
        list_prod_status=list_prod_status
    )


def tinhTien():
    total = request.get_json().get("subTotal")
    extra_total=RuleService.RuleService.calulate_service_fee(total)
    return jsonify({
        "status": "success",
        "extra_total": extra_total,
        "final_total": total + extra_total
    })

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
    return render_template("page/cart.html", tab=tab, list_pro=cart_item, list_order=list_prod)

def remove_product_in_cart():
    product_id=request.get_json().get('product_id')
    CartDao.remove_product_in_cart_dao(product_id, current_user.id)
    return jsonify({
        "status": "success",
        "message": "Đã xoá sản phẩm khỏi giỏ hàng"
    })