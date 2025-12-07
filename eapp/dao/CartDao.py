from eapp import db, app
from eapp.models.Cart import Cart


def get_cart_by_user(user_id):
    return Cart.query.filter_by(user_id=user_id).first()


def created_cart_dao(user_id):
    # 1. Kiểm tra cart đã tồn tại chưa
    existing_cart = get_cart_by_user(user_id)
    if existing_cart:
        return existing_cart   # ❗ trả về cart cũ, không tạo cart mới

    # 2. Nếu chưa có → tạo mới
    cart = Cart(user_id=user_id)
    try:
        db.session.add(cart)
        db.session.commit()
        return cart
    except Exception as e:
        db.session.rollback()
        print("Error creating cart:", e)
        return None
