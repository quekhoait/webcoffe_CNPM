from eapp import db
from eapp.models.Cart import Cart
from eapp.models.Product import Product
from eapp.models.CartDetail import CartDetail
from eapp.dao import ProductDao
from eapp.services.RuleService import RuleService

def get_cart_by_user(user_id):
    return Cart.query.filter_by(user_id=user_id).first()

def create_cart_dao(user_id):
    cart = get_cart_by_user(user_id)
    if cart:
        return cart
    cart = Cart(user_id=user_id)
    try:
        db.session.add(cart)
        db.session.commit()
        return cart
    except Exception as e:
        db.session.rollback()
        print("Error creating cart:", e)
        return None


def get_cart_item(cart_id, product_id):
    return CartDetail.query.filter_by(cart_id=cart_id, product_id=product_id).first()


def add_to_cart_dao(product_id, user_id, quantity):
    product = ProductDao.get_by_id(product_id)
    if product is None:
        return {"success": False, "message": "Sản phẩm không tồn tại"}
    # Lấy cart (nếu chưa có thì tạo mới)
    cart = create_cart_dao(user_id)
    cart_item = get_cart_item(cart.id, product_id)

    if cart_item:
        # nếu đã có → tăng số lượng
        cart_item.quantity += quantity
    else:
        # chưa có → thêm mới
        cart_item = CartDetail(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            unit_price=product.price,
            total_price=product.price * quantity
        )
    db.session.add(cart_item)
    db.session.commit()
    return cart_item

# Lấy tất cả product trong cartdetail
def get_cart_by_userId_dao(user_id):
    return (
        CartDetail.query
        .join(Cart, CartDetail.cart_id == Cart.id)
        .join(Product, CartDetail.product_id == Product.id)
        .filter(Cart.user_id == user_id)
        .all()
    )

def remove_product_in_cart_dao(product_id, user_id):
    cart_item = (CartDetail.query
                 .join(Cart, CartDetail.cart_id == Cart.id)
                 .filter(CartDetail.product_id == product_id, Cart.user_id==user_id).first()
                 )
    if not cart_item:
        return False
    db.session.delete(cart_item)
    db.session.commit()
    return True