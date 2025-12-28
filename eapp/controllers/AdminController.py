from flask import render_template, request, jsonify
import cloudinary.uploader
import json
from eapp.dao import ProductDao, CategoryDao
from eapp.dao.IngredientDAO import IngredientDAO

def load_product():
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
            'name': name,
            'price': float(price),
            'unit': unit,
            'dish_category_id': category_id,
            'description': description,
            'image': image_url
        }

        if ProductDao.add_product(data, recipes):
            return jsonify({'success': True, 'message': 'Thêm món thành công!'})
        return jsonify({'success': False, 'message': 'Lỗi Database!'})
    except Exception as e:
        print(e)
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

        data = {
            'name': name,
            'price': float(price),
            'unit': unit,
            'dish_category_id': category_id,
            'description': description
        }

        #chỉ cập nhật nếu có ảnh mới gửi lên
        if image_file:
            res = cloudinary.uploader.upload(image_file)
            data['image'] = res.get('secure_url')

        if ProductDao.update_product(product_id, data):
            return jsonify({'success': True, 'message': 'Cập nhật thành công!'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi cập nhật!'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


def api_delete_product():
    data = request.json
    if ProductDao.delete_product(data.get('id')):
        return jsonify({'success': True, 'message': 'Xóa thành công!'})
    return jsonify({'success': False, 'message': 'Lỗi xóa!'})



def api_add_category():
    data = request.json
    name = data.get('name')
    description = data.get('description')
    if not name or not description:
        return jsonify({'success': False, 'message': 'Nhập đầy đủ thông tin!'})

    new_cat = CategoryDao.create_category(name, description)

    if new_cat:
        return jsonify({
            'success': True,
            'message': 'Thêm danh mục thành công!',
            'category': {
                'id': new_cat.id,
                'name': new_cat.name,
                'description': new_cat.description
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Lỗi: Danh mục đã tồn tại hoặc lỗi server!'})

def api_update_category():
        data = request.get_json()
        id = data.get('id')
        print("id", id)
        name = data.get('name')
        description = data.get('description')
        if not name or not description:
            return jsonify({'success': False, 'message': 'Nhập đầy đủ thông tin!'})
        print("id", id)
        new_cat = CategoryDao.update_categories_dao(id, name, description)

        if new_cat:
            return jsonify({
                'success': True,
                'message': 'cập nhật danh mục thành công!',
                'category': {
                    'id': new_cat.id,
                    'name': new_cat.name,
                    'description': new_cat.description
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Lỗi: Danh mục đã tồn tại hoặc lỗi server!'})