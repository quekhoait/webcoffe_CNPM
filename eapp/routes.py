# Cấu trúc route của các trang web bình thường

from flask import Flask, render_template
# Thay đổi import tương đối thành import tuyệt đối:
# from eapp.dao.Product import get_product
from eapp import app
from eapp.controllers import CashierController, ProductController, StaffController, index


app.add_url_rule('/about-us','about-us',index.aboutUs)
# app.add_url_rule('/','index',index.loadHome)
# demo
app.add_url_rule('/staff','index2',StaffController.load_staff)
app.add_url_rule('/','index',CashierController.home)



app.add_url_rule('/api/dish','dish',ProductController.list)
# staff
app.add_url_rule('/staff','staff',StaffController.load_staff)
app.add_url_rule('/api/order','add_order',StaffController.addItemToInvoice, methods=['post'])
app.add_url_rule('/api/invoice','create_invoice',StaffController.create_invoice, methods=['post'])
app.add_url_rule('/api/remove-item','remove_item',StaffController.removeItemFromInvoice, methods=['post'])
#cashier

