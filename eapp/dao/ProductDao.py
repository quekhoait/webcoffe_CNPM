from MySQLdb._mysql import result
from sqlalchemy.sql.functions import current_user

from eapp.models import Product, CartDetail, Invoice, Payment, InvoiceDetail
from sqlalchemy import desc

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


def get_product_by_status_dao(user_id, invoice_status=None, payment_status=None):
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
    result = query.with_entities(
        Product,
        Invoice,
        Payment
    ).all()
    return result
