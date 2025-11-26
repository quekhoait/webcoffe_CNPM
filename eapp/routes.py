# Cấu trúc route của các trang web bình thường

from flask import Flask, render_template
# Thay đổi import tương đối thành import tuyệt đối:
# from eapp.dao.Product import get_product
from eapp import app
from eapp.controllers import DishController, index

# @app.context_processor
# def global_data():
#     return dict(
#         primary_color='#'
#     )


# @app.route('/')
# def home():
#     # products_list = get_product()
#     return render_template('page/home.html', )
app.add_url_rule('/','index',index.home)
app.add_url_rule('/api/dish','dish',DishController.list)
