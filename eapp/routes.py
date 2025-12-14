# Cấu trúc route của các trang web bình thường
from msilib import CAB

from flask import Flask, render_template
# Thay đổi import tương đối thành import tuyệt đối:
# from eapp.dao.Product import get_product
from eapp import app
from eapp.controllers import AccountController, CashierController, ProductController, StaffController, WarehouseController, index, \
    CartController, PaymentController

app.add_url_rule('/login','login', index.load_login)
app.add_url_rule('/api/login','login_account',AccountController.login, methods=['POST'])
app.add_url_rule('/regis','register', index.load_regis)
app.add_url_rule('/api/regis','created_account',AccountController.register, methods=['POST'])
app.add_url_rule('/logout','logout', AccountController.logout)
app.add_url_rule('/api/check_password','check_password', AccountController.check_password, methods=['POST'])
app.add_url_rule('/api/update_account','update_account', AccountController.update_account, methods=['POST'])

# Load trang
app.add_url_rule('/profile','profile', index.load_profile)
app.add_url_rule('/','index',index.load_home)
app.add_url_rule('/about-us','about-us',index.load_about_us)


#Xử lý giỏ hàng
app.add_url_rule('/my-cart','my-cart',CartController.load_my_cart)
app.add_url_rule('/api/add_to_cart', 'add_to_cart', CartController.add_to_cart, methods=['POST'])
app.add_url_rule('/api/get-cart-by-userId','get-cart-by-userId',CartController.get_cart_by_userId)
# demo
app.add_url_rule('/staff','index2',StaffController.load_staff)
# app.add_url_rule('/','index',CashierController.home)



app.add_url_rule('/api/products','products',ProductController.list('/staff/product_item.html'), methods=['get'])

# staff

app.add_url_rule('/staff','staff',StaffController.load_staff)
app.add_url_rule('/api/order','add_order',StaffController.addItemToInvoice, methods=['post'])
app.add_url_rule('/api/invoice','create_invoice',StaffController.create_invoice, methods=['post'])
app.add_url_rule('/api/remove-item','remove_item',StaffController.removeItemFromInvoice, methods=['post'])



#menu
app.add_url_rule('/menu', 'menu', index.load_menu, methods=['GET'])
app.add_url_rule('/api/get_product', 'get_product', ProductController.get_product, methods=['GET'])


#thanh toan
app.add_url_rule('/payment', 'payment', PaymentController.load_data, methods=['POST', 'GET'])
app.add_url_rule('/api/created_payment', 'created_payment', PaymentController.created_payment, methods=['POST'])

#cashier
app.add_url_rule('/cashier','cashier',CashierController.load_cashier)
app.add_url_rule('/cashier/status-bar', 'get_status_bar', CashierController.load_status_bar, methods=['get'])

# app.add_url_rule('/product/<int:id>', 'product_detail', index.product_detail, methods=['GET'])


app.add_url_rule('/warehouse', 'warehouse', WarehouseController.warehouse_page)
app.add_url_rule('/admin/warehouse/create-ticket', 'create_ticket', StaffController.create_ticket, methods=['POST'])


#API Ingredient
app.add_url_rule('/api/ingredients', 'get_ingredients', WarehouseController.get_ingredients, methods=['GET'])

#API WarehouseSlip
app.add_url_rule('/api/warehouse-slips', 'create_warehouse_slip', WarehouseController.create_warehouse_slip, methods=['POST'])

#API Invoice
app.add_url_rule('/api/invoices', 'get_invoices', CashierController.load_invoices, methods=['get'])
app.add_url_rule('/api/invoice-detail', 'get_invoice_detail', CashierController.load_invoice_detail, methods=['get'])
