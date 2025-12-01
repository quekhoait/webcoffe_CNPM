# Cấu trúc route của các trang web bình thường

from flask import Flask, render_template
# Thay đổi import tương đối thành import tuyệt đối:
# from eapp.dao.Product import get_product
from eapp import app
from eapp.controllers import ProductController, StaffController, index, AccountController


app.add_url_rule('/login','login', index.load_login)
app.add_url_rule('/api/login','login_account',AccountController.login, methods=['POST'])

app.add_url_rule('/regis','register', index.load_regis)
app.add_url_rule('/api/regis','created_account',AccountController.register, methods=['POST'])
from eapp.controllers import CashierController, ProductController, StaffController, index

app.add_url_rule('/logout','logout', AccountController.logout)

app.add_url_rule('/profile','profile', index.load_profile)
app.add_url_rule('/api/check_password','check_password', AccountController.check_password, methods=['POST'])




app.add_url_rule('/','index',index.load_home)
app.add_url_rule('/about-us','about-us',index.load_about_us)
# app.add_url_rule('/','index',index.loadHome)
# demo
app.add_url_rule('/staff','index2',StaffController.load_staff)
# app.add_url_rule('/','index',CashierController.home)



app.add_url_rule('/api/dish','dish',ProductController.list)
# staff
app.add_url_rule('/staff','staff',StaffController.load_staff)
app.add_url_rule('/api/order','add_order',StaffController.addToOrder, methods=['post'])
app.add_url_rule('/api/invoice','create_invoice',StaffController.create_invoice, methods=['post'])

#cashier

