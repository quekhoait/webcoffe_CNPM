# Cấu trúc route của các trang web bình thường

from flask import Flask, render_template
# Thay đổi import tương đối thành import tuyệt đối:
# from eapp.dao.Product import get_product
from eapp import app
from eapp.controllers import DishController, index


app.add_url_rule('/about-us','about-us',index.aboutUs)
app.add_url_rule('/','index',index.loadHome)
app.add_url_rule('/api/dish','dish',DishController.list)
