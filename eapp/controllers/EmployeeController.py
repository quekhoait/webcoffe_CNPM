from flask import render_template, jsonify
from eapp.dao import AccountDAO
from cloudinary.provisioning import users

from flask import render_template, jsonify, request
from eapp.dao import AccountDAO
from eapp.models.Account import Role




def index():
    try:
        users = AccountDAO.get_all_employees()
    except Exception as e:
        print(f"Lỗi: {e}")
        users = []

    return render_template('admin/admin.html', users=users, roles=Role)


def api_add():
    data = request.json
    try:
        #ktra trùng SĐT
        if AccountDAO.check_phone_exists(data['phone']):
            return jsonify({'success': False, 'message': 'Số điện thoại này đã được sử dụng!'})


        role_map = {
            'STAFF': Role.STAFF,
            'CASHIER': Role.CASHIER,
            'WAREHOUSE_KEEPER': Role.WAREHOUSE_KEEPER,
            'ADMIN': Role.ADMIN
        }
        selected_role = role_map.get(data['role'], Role.STAFF)

        AccountDAO.create_employee(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            password=data.get('password', '123456'),
            role_enum=selected_role,
            address=data.get('address')
        )
        return jsonify({'success': True, 'message': 'Thêm nhân viên thành công!'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Lỗi server: ' + str(e)})

    data = request.json
    try:
        #ktra trùng SĐT
        if AccountDAO.check_phone_exists(data['phone']):
            return jsonify({'success': False, 'message': 'Số điện thoại này đã được sử dụng!'})


        role_map = {
            'STAFF': Role.STAFF,
            'CASHIER': Role.CASHIER,
            'WAREHOUSE_KEEPER': Role.WAREHOUSE_KEEPER,
            'ADMIN': Role.ADMIN
        }
        selected_role = role_map.get(data['role'], Role.STAFF)

        AccountDAO.create_employee(
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            password=data.get('password', '123456'),
            role_enum=selected_role,
            address=data.get('address')
        )
        return jsonify({'success': True, 'message': 'Thêm nhân viên thành công!'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Lỗi server: ' + str(e)})


def api_update():
    data = request.json
    try:
        role_map = {
            'STAFF': Role.STAFF,
            'CASHIER': Role.CASHIER,
            'WAREHOUSE_KEEPER': Role.WAREHOUSE_KEEPER,
            'ADMIN': Role.ADMIN
        }
        selected_role = role_map.get(data['role'])

        success = AccountDAO.update_employee_info(
            user_id=data['id'],
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            role_enum=selected_role,
            address=data.get('address'),
            status=data['active'],
            password=data.get('password')
        )

        if success:
            return jsonify({'success': True, 'message': 'Cập nhật thành công!'})
        else:
            return jsonify({'success': False, 'message': 'Không tìm thấy nhân viên!'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Lỗi server: ' + str(e)})

    data = request.json
    try:
        role_map = {
            'STAFF': Role.STAFF,
            'CASHIER': Role.CASHIER,
            'WAREHOUSE_KEEPER': Role.WAREHOUSE_KEEPER,
            'ADMIN': Role.ADMIN
        }
        selected_role = role_map.get(data['role'])

        success = AccountDAO.update_employee_info(
            user_id=data['id'],
            name=data['name'],
            phone=data['phone'],
            email=data['email'],
            role_enum=selected_role,
            address=data.get('address'),
            status=data['active'],
            password=data.get('password')
        )

        if success:
            return jsonify({'success': True, 'message': 'Cập nhật thành công!'})
        else:
            return jsonify({'success': False, 'message': 'Không tìm thấy nhân viên!'})
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': 'Lỗi server: ' + str(e)})


def api_delete():
    data = request.json
    try:
        if AccountDAO.delete_employee_dao(data['id']):
            return jsonify({'success': True, 'message': 'Đã khóa tài khoản nhân viên!'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi xóa!'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Lỗi hệ thống: ' + str(e)})


    data = request.json
    try:
        if AccountDAO.delete_employee_dao(data['id']):
            return jsonify({'success': True, 'message': 'Đã khóa tài khoản nhân viên!'})
        else:
            return jsonify({'success': False, 'message': 'Lỗi khi xóa!'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Lỗi hệ thống: ' + str(e)})

