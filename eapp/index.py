from eapp import app
# from eapp.models. import Product
# from eapp.models.BaseModel import BaseModel
# from eapp.models.CategoryModel import Categories
# from eapp.dao.Product import add_product



if __name__ == '__main__':
    # Tạo Application Context để Flask biết nó đang chạy trong môi trường ứng dụng nào
    with app.app_context():
        # db.create_all()
        # print("Đã tạo bảng cơ sở dữ liệu thành công!")
        # add_product()
        app.run(debug=True)