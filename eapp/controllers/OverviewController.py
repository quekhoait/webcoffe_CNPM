from flask import request, jsonify, render_template
from datetime import datetime
from eapp.dao import OverviewDAO

# Laaysy doanh thu theo thời gian
def load_overview():
        # Lấy query params
        time_type = request.args.get('type', 'day')
        start_time = request.args.get('start_time')
        end_time = request.args.get('end_time')

        # Xử lý time_value
        time_value = None
        if start_time and end_time:
            start = datetime.fromisoformat(start_time)
            end = datetime.fromisoformat(end_time)
            time_value = (start, end)
            time_type = 'range'
        elif start_time:
            time_value = datetime.fromisoformat(start_time)

        # Tổng doanh thu
        total_revenue = OverviewDAO.revenue_by_time_dao(time_type, time_value)

        # Top sản phẩm
        data = OverviewDAO.top_products_by_time_dao(time_type=time_type, time_value=time_value)
        result = [{
            'product_id': item.product_id,
            'product_name': item.product_name,
            'total_quantity': int(item.total_quantity),
            'total_revenue': float(item.total_revenue)
        } for item in data]

        return render_template(
            'admin/overview.html',
            tab=time_type,
            total_revenue=total_revenue,
            result=result
        )
# {
#   'total_revenue': 375000.0,
#   'total_orders': 3
# }


# [
#     {
#         "product_id": 1,
#         "product_name": "Cà Phê Đen",
#         "total_quantity": 2,
#         "total_revenue": 100000.0
#     },
#     {
#         "product_id": 2,
#         "product_name": "Cà Phê Sữa",
#         "total_quantity": 1,
#         "total_revenue": 20000.0
#     }
# ]