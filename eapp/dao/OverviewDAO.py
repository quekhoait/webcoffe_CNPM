from sqlalchemy import func
from datetime import datetime
from eapp import db
from eapp.models import Invoice, InvoiceDetail, Product

#:lấy doanh thu theo thời gian
def revenue_by_time_dao(time_type='day', time_value='None' ):
    # Truy vấn doanh thu
    revenue_query = db.session.query(func.sum(Invoice.final_total).label('total_revenue'))
    revenue_query = revenue_query.filter(Invoice.invoice_status == 'completed')

    # Truy vấn số đơn hàng
    order_query = db.session.query(func.count(Invoice.id).label('total_orders'))
    order_query = order_query.filter(Invoice.invoice_status == 'completed')

    # Xử lý theo thời gian
    if time_type == 'day':
        if not time_value:
            time_value = datetime.now()
        revenue_query = revenue_query.filter(func.date(Invoice.created_date) == time_value.date())
        order_query = order_query.filter(func.date(Invoice.created_date) == time_value.date())
    elif time_type == 'month':
        if not time_value:
            time_value = datetime.now()
        revenue_query = revenue_query.filter(func.extract('year', Invoice.created_date) == time_value.year)
        revenue_query = revenue_query.filter(func.extract('month', Invoice.created_date) == time_value.month)
        order_query = order_query.filter(func.extract('year', Invoice.created_date) == time_value.year)
        order_query = order_query.filter(func.extract('month', Invoice.created_date) == time_value.month)
    elif time_type == 'year':
        if not time_value:
            time_value = datetime.now()
        revenue_query = revenue_query.filter(func.extract('year', Invoice.created_date) == time_value.year)
        order_query = order_query.filter(func.extract('year', Invoice.created_date) == time_value.year)
    elif time_type == 'range':
        start, end = time_value
        revenue_query = revenue_query.filter(Invoice.created_date >= start, Invoice.created_date <= end)
        order_query = order_query.filter(Invoice.created_date >= start, Invoice.created_date <= end)

    total_revenue = revenue_query.scalar() or 0
    total_orders = order_query.scalar() or 0

    return {
        'total_revenue': total_revenue,
        'total_orders': total_orders
    }


def top_products_by_time_dao(time_type='day', time_value=None):
    # Mặc định thời gian hiện tại nếu không truyền
    if not time_value:
        time_value = datetime.now()

    # Base query: join InvoiceDetail với Invoice và Product
    query = db.session.query(
        InvoiceDetail.product_id,
        Product.name.label('product_name'),
        func.sum(InvoiceDetail.quantity).label('total_quantity'),
        func.sum(InvoiceDetail.quantity * InvoiceDetail.price).label('total_revenue')
    ).join(Invoice, Invoice.id == InvoiceDetail.invoice_id
           ).join(Product, Product.id == InvoiceDetail.product_id
                  ).filter(Invoice.invoice_status == 'completed')

    # Lọc theo thời gian
    if time_type == 'day':
        query = query.filter(func.date(Invoice.created_date) == time_value.date())
    elif time_type == 'month':
        query = query.filter(func.extract('year', Invoice.created_date) == time_value.year)
        query = query.filter(func.extract('month', Invoice.created_date) == time_value.month)
    elif time_type == 'year':
        query = query.filter(func.extract('year', Invoice.created_date) == time_value.year)
    elif time_type == 'range':
        start, end = time_value
        query = query.filter(Invoice.created_date >= start, Invoice.created_date <= end)

    # Nhóm theo sản phẩm và sắp xếp theo số lượng bán
    query = query.group_by(InvoiceDetail.product_id, Product.name
                           ).order_by(func.sum(InvoiceDetail.quantity).desc()
                                      )

    return query.all()