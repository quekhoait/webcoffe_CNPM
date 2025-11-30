from flask import render_template, request, redirect, jsonify, session, url_for
from flask_login import login_user, logout_user
from eapp import app, dao,  utils
import math


def register():    
    username = request.form.get("username")
    phone = request.form.get("phone")
    name = request.form.get("name")
    password = request.form.get("password")
    confirm = request.form.get("confirm")

    if not username or not phone or not name or not password or not confirm:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ giá trị!"})
    if password != confirm:
        return jsonify({"status": "error", "message": "Mật khẩu xác nhận không khớp!"})
    try:
        dao.AccountDao.add_account(username=username, phone=phone, name=name, password=password)
        return jsonify({"status": "ok"})
    except Exception as ex:
        app.logger.error(f'Lỗi khi thêm tài khoản: {ex}')
        return jsonify({"status": "error", "message": "Có lỗi xảy ra, thử lại sau!"})
