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


#menu
app.add_url_rule('/menu', 'menu', index.menu_page, methods=['GET'])
#thanh toan
app.add_url_rule('/checkout', 'checkout', index.checkout_page, methods=['GET', 'POST'])

app.add_url_rule('/product/<int:id>', 'product_detail', index.product_detail, methods=['GET'])


app.add_url_rule('/admin/warehouse', 'warehouse', StaffController.warehouse_page)
app.add_url_rule('/admin/warehouse/create-ticket', 'create_ticket', StaffController.create_ticket, methods=['POST'])