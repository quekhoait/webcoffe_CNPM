from flask import render_template, session, request, redirect, url_for
from eapp import db
from datetime import datetime

from sqlalchemy import desc #hàm sx giảm dần

from eapp.dao import CategoryDao, ProductDao, AccountDAO
from eapp.models import Category
from flask import render_template, request
from eapp.models.Account import Role
from eapp.services.inventory.InventoryValidator import InventoryValidator
from eapp.models import Product, ProductStatus


def load_login():
    return render_template('page/login.html')


def load_regis():
    return render_template('page/register.html')

def load_home():
    categories = Category.query.limit(4).all()

    featured_products = Product.query.filter_by(status=ProductStatus.ACTIVE) \
        .limit(8).all()

    menu_products = Product.query.filter_by(status=ProductStatus.ACTIVE).limit(10).all()

    return render_template('page/home.html',
                           categories=categories,
                           featured_products=featured_products,
                           menu_products=menu_products)
    # products = ProductDao.list()
    # return render_template('page/home.html', products=products)


def load_about_us():

    return render_template('page/about_us.html')





def load_menu():
    # /menu?name=cafe&category_id=1&filter=new
    search_query = request.args.get('name', '')  #từ khóa tìm kiếm
    category_id = request.args.get('category_id')  #id danh mục
    filter_type = request.args.get('filter')  #lọc
    params = request.args.to_dict()
    categories = CategoryDao.list()

    products = ProductDao.list(params)
    product_makeable_map = InventoryValidator.get_product_makeable_map(products,get_current_warehouse())
    return render_template('page/menu.html',
                           products=products,
                           categories=categories,
                           # Gửi lại các tham số để View biết cái nào đang được chọn
                           current_cate_id=int(category_id) if category_id else None,
                           current_filter=filter_type,
                           search_query=search_query,
                           product_makeable_map=product_makeable_map)

def load_profile():
    tab = request.args.get("tab", "profile")
    return render_template("page/profile.html", tab=tab)



def load_my_cart():
    return render_template('page/cart.html')

def get_current_warehouse():
    return 1

def load_admin():
    return render_template('admin/admin.html')

def load_employee():
    try:
        users = AccountDAO.get_all_employees()
        # users = AccountDAO.get_all_employees()
        # chuyen doi tuong user thanh json (dict)
        # ra hieu dong nay ne sep
        users = [ u.to_dict() for u in AccountDAO.get_all_employees() ]

    except Exception as e:
        users = []
    return render_template('admin/employee_manage.html', users=users, roles=Role)

def load_overview():
    return render_template('admin/overview.html')



def load_product_detail(id):

    product = Product.query.get(id)

    if not product:
        return "Không tìm thấy sản phẩm", 404

    related_products = Product.query.filter(
        Product.dish_category_id == product.dish_category_id,
        Product.id != product.id
    ).limit(4).all()

    return render_template('page/product_detail.html',
                           product=product,
                           related_products=related_products)