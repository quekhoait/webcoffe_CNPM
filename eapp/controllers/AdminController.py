from flask import render_template, request, jsonify
import cloudinary.uploader
from eapp.dao import ProductDao, CategoryDao



def index():
    products = ProductDao.list()
    categories = CategoryDao.list()
    return render_template('admin/product_manage.html', products=products, categories=categories)


def api_add_product():
    try:
        name = request.form.get('name')
        price = request.form.get('price')
        unit = request.form.get('unit')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        image_file = request.files.get('image')

        if not name or not price:
            return jsonify({'success': False, 'message': 'Tên và giá là bắt buộc!'})

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

        if ProductDao.add_product(data):
            return jsonify({'success': True, 'message': 'Thêm mới thành công!'})
        else:
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
    try:
        data = request.json
        if ProductDao.delete_product(data.get('id')):
            return jsonify({'success': True, 'message': 'Xóa thành công!'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi xóa!'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})