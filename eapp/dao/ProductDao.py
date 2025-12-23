from eapp.models import Product, ProductRecipe, ProductRecipe, ProductStatus
# from MySQLdb._mysql import result
from sqlalchemy.sql.functions import current_user

from eapp.models import Product, CartDetail, Invoice, Payment, InvoiceDetail, ProductRecipe
from sqlalchemy import desc
from eapp import db


def list(params: dict = None):
    try:
        query = Product.query
        if params:
            if 'category_id' in params:
                query = query.filter(Product.dish_category_id == params['category_id'])

            if 'name' in params:
                query = query.filter(Product.name.contains(params['name']))

            if 'filter' in params:
                if params['filter'] == 'new':
                    # sx theo ngày tạo giảm dần
                    query = query.order_by(desc(Product.created_date))
                elif params['filer'] == 'best':
                    # sx theo số lượt đánh giá giảm dần
                    query = query.order_by(desc(Product.rating_count))

        return query.all()

    except Exception as ex:
        print(f"Lỗi khi lọc món: {ex}")
        return []
    

def get_by_id(id):
    try:
        return Product.query.get(id)
    except Exception as ex:
        print(f"Lỗi khi món theo id: {ex}")
        return None

def get_product_recipe_map():
    products = list()
    product_recipe = {}

    for product in products:
        product_recipe[product.id] = [
            {'ingredient_id' : ing.ingredient_id, 'quantity' : ing.quantity}
            for ing in product.ingredients
        ]

    return product_recipe


def get_product_by_status_dao(user_id, invoice_status=None, payment_status=None, search_key=None):
    query = (
        Invoice.query
        .join(Payment, Payment.invoice_id == Invoice.id)
        .join(InvoiceDetail, InvoiceDetail.invoice_id == Invoice.id)
        .join(Product, Product.id == InvoiceDetail.product_id)
        .filter(Invoice.customer_id == user_id)
    )

    if invoice_status is not None:
        query = query.filter(Invoice.invoice_status == invoice_status)
    if payment_status is not None:
        query = query.filter(Payment.status == payment_status)
    if search_key:  # thêm điều kiện tìm kiếm
        query = query.filter(Product.name.ilike(f"%{search_key}%"))

    result = query.with_entities(
        Product,
        Invoice,
        Payment
    ).all()
    return result



def add_product(data, recipes=[]):
    try:
        new_product = Product(
            name=data.get('name'),
            price=data.get('price'),
            unit=data.get('unit'),
            dish_category_id=data.get('dish_category_id'),
            description=data.get('description'),
            image=data.get('image')
        )
        db.session.add(new_product)
        db.session.flush()
        #lưu công thức
        for item in recipes:
            if item.get('ingredient_id'):
                recipe = ProductRecipe(
                    product_id=new_product.id,
                    ingredient_id=item['ingredient_id'],
                    quantity=item['quantity'],
                    unit=item['unit']
                )
                db.session.add(recipe)

        db.session.commit()
        return True
    except Exception as ex:
        print(f"Lỗi thêm: {ex}")
        db.session.rollback()
        return False

def update_product(product_id, data, recipes=None):
    try:
        product = Product.query.get(product_id)
        if not product: return False

        product.name = data.get('name')
        product.price = data.get('price')
        product.unit = data.get('unit')
        product.dish_category_id = data.get('dish_category_id')
        product.description = data.get('description')
        if data.get('image'):
            product.image = data.get('image')

        #cập nhật công thức nếu có
        if recipes is not None:
            #xóa công thức cũ -> thêm công thức mới
            ProductRecipe.query.filter_by(product_id=product_id).delete()
            for item in recipes:
                if item.get('ingredient_id'):
                    new_recipe = ProductRecipe(
                        product_id=product.id,
                        ingredient_id=item['ingredient_id'],
                        quantity=item['quantity'],
                        unit=item['unit']
                    )
                    db.session.add(new_recipe)

        db.session.commit()
        return True
    except Exception as ex:
        print(f"Lỗi sửa: {ex}")
        db.session.rollback()
        return False

def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if product:
            ProductRecipe.query.filter_by(product_id=product_id).delete()
            db.session.delete(product)
            db.session.commit()
            return True
        return False
    except Exception as ex:
        db.session.rollback()
        return False


