from flask import render_template, request, jsonify
import cloudinary.uploader
import json
from eapp.dao import ProductDao, CategoryDao
from eapp.dao.IngredientDAO import IngredientDAO


def index():
    products_db = ProductDao.list()
    products = [p.to_dict() for p in products_db]

    categories = CategoryDao.list()
    ingredients = IngredientDAO.list()

    return render_template('admin/product_manage.html',
                           products=products,
                           categories=categories,
                           ingredients=ingredients)


def api_add_product():
    try:
        name = request.form.get('name')
        price = request.form.get('price')
        unit = request.form.get('unit')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        image_file = request.files.get('image')
        #dịch chuỗi json từ js gửi lên thành list
        recipes = json.loads(request.form.get('recipes', '[]'))

        image_url = "https://via.placeholder.com/150"
        if image_file:
            res = cloudinary.uploader.upload(image_file)
            image_url = res.get('secure_url')

        data = {
            'name': name, 'price': float(price), 'unit': unit,
            'dish_category_id': category_id, 'description': description, 'image': image_url
        }

        if ProductDao.add_product(data, recipes):
            return jsonify({'success': True, 'message': 'Thêm món thành công!'})
        return jsonify({'success': False, 'message': 'Lỗi Database!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


def api_update_product():
    try:
        product_id = request.form.get('id')
        name = request.form.get('name')
        price = request.form.get('price')
        unit = request.form.get('unit')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        image_file = request.files.get('image')
        recipes = json.loads(request.form.get('recipes')) if request.form.get('recipes') else []

        data = {
            'name': name, 'price': float(price), 'unit': unit,
            'dish_category_id': category_id, 'description': description
        }

        if image_file:
            res = cloudinary.uploader.upload(image_file)
            data['image'] = res.get('secure_url')

        if ProductDao.update_product(product_id, data, recipes):
            return jsonify({'success': True, 'message': 'Cập nhật thành công!'})
        return jsonify({'success': False, 'message': 'Lỗi cập nhật!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


def api_delete_product():
    data = request.json
    if ProductDao.delete_product(data.get('id')):
        return jsonify({'success': True, 'message': 'Xóa thành công!'})
    return jsonify({'success': False, 'message': 'Lỗi xóa!'})


