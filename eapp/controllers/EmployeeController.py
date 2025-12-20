from flask import render_template, jsonify
from eapp.dao import AccountDAO
from eapp.models.Account import Role


def index():
    try:
        users = AccountDAO.get_all_employees()
    except Exception as e:
        users = []

    return render_template('admin/employee_manage.html', users=users, roles=Role)


def api_add():
    return jsonify({'success': False, 'message': '...'})

def api_update():
    return jsonify({'success': False, 'message': '...'})

def api_delete():
    return jsonify({'success': False, 'message': '...'})

