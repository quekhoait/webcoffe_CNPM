# Cấu trúc route của các trang web bình thường

from flask import Flask, render_template
# Thay đổi import tương đối thành import tuyệt đối:
# from eapp.dao.Product import get_product
from eapp import app
from eapp.controllers import ProductController, StaffController, index


app.add_url_rule('/about-us','about-us',index.aboutUs)
app.add_url_rule('/','index',index.loadHome)

app.add_url_rule('/api/dish','dish',ProductController.list)
# staff
app.add_url_rule('/staff','staff',StaffController.load_staff)
app.add_url_rule('/api/order','add_order',StaffController.addToOrder, methods=['post'])
app.add_url_rule('/api/invoice','create_invoice',StaffController.create_invoice, methods=['post'])

#thanh toan
app.add_url_rule('/login-test', 'login_test', index.login_test)
app.add_url_rule('/checkout', 'checkout', index.checkout_page, methods=['GET', 'POST'])