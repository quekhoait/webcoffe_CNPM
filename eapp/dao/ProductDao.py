from sqlalchemy.sql.functions import current_user

from eapp.models import Product, CartDetail, Invoice, Payment
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


def get_product_by_status_dao(invoice_status=None, payment_status=None):
    query = Invoice.query.join(Payment, Payment.invoice_id == Invoice.id)
    query = query.filter(Invoice.customer_id == current_user.id)
    if invoice_status is not None:
        query = query.filter(Invoice.invoice_status == invoice_status)
    if payment_status is not None:
        query = query.filter(Payment.status == payment_status)
    list_prod = query.all()
    return list_prod