#nhận request từ giao diện post, get
from flask import app, jsonify, render_template, request

from eapp.dao import ProductDao



# @app.route('/api/dish', methods=['get'])
def list(filehtml):
    """
    Đây là hàm KHỞI TẠO, nó nhận tên file HTML và TRẢ VỀ VIEW FUNCTION.

    :param filehtml: Tên template HTML sẽ được render.
    """

    def view_function():
        """
        VIEW FUNCTION THỰC TẾ: Hàm này chỉ chạy khi có HTTP Request.
        """
        # Lệnh này chỉ hợp lệ khi ở trong Request Context
        # print(request) # Có thể in request ở đây nếu muốn gỡ lỗi

        params = request.args.to_dict()

        # Lấy dữ liệu (Giả định ProductDao đã được định nghĩa)
        products = ProductDao.list(params)
        # Render template đã được chỉ định (filehtml) với dữ liệu
        return render_template(filehtml, products=products)

    # Hàm list() trả về view_function (Closure)
    return view_function


def get_product():
    params = request.args.to_dict()
    # re2=DishDAO.list(params)
    # result = [d.to_dict() for d in DishDAO.list(params)]
    dishes = ProductDao.list(params)
    # import pdb
    # pdb.set_trace
    # return jsonify(result),200
    return jsonify([d.to_dict() for d in dishes]), 200


