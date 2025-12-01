from flask import render_template, request, redirect, jsonify, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from eapp import app, utils
import math, re, hashlib
from eapp.dao.AccountDao import add_account, check_phone_exists, login_account
from werkzeug.security import check_password_hash


def register():    
    username = request.form.get("username")
    phone = request.form.get("phone")
    name = request.form.get("name")
    password = request.form.get("password")
    confirm = request.form.get("confirm")

    phone_regex = r"^0\d{9}$"
    if not username or not phone or not name or not password or not confirm:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ giá trị!"})
    if not re.match(phone_regex, phone):
        return jsonify({"status": "error", "message": "Số điện thoại không hợp lệ!"})
    if len(password) < 6:
        return jsonify(({"status": "error", "message":"Mật khẩu phải hơn 6 ký tự!"}))
    if password != confirm:
        return jsonify({"status": "error", "message": "Mật khẩu xác nhận không khớp!"})
    if check_phone_exists(phone):
        return jsonify(({"status":"error", "message": "Số điện thoại đã tồn tại!"}))
    try:
        add_account(username=username, phone=phone, name=name, password=password)
        return jsonify({"status": "success"})
    except Exception as ex:
        app.logger.error(f'Lỗi khi thêm tài khoản: {ex}')
        return jsonify({"status": "error", "message": "Có lỗi xảy ra, thử lại sau!"})


def login():
    phone = request.form.get("phone")
    password = request.form.get("password")
    phone_regex = r"^0\d{9}$"
    if not phone or not password:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ giá trị!"})
    if not re.match(phone_regex, phone):
        return jsonify({"status": "error", "message": "Số điện thoại không hợp lệ!"})
    if len(password) < 6:
        return jsonify({"status": "error", "message": "Mật khẩu phải hơn 6 ký tự!"})
    try:
        u = login_account(phone=phone, password=password)
        if not u:
            return jsonify({"status": "error", "message": "Sai số điện thoại hoặc mật khẩu!"})

        # login_user là của flask_login
        login_user(u)
        return jsonify({"status": "success", "message": "Đăng nhập thành công!"})
    except Exception as ex:
        app.logger.error(f'Lỗi khi đăng nhập: {ex}')
        return jsonify({"status": "error", "message": "Có lỗi xảy ra, thử lại sau!"})

def logout():
    logout_user()
    return redirect('/')

def check_password():
    data = request.get_json()
    password = data.get("password", "").strip()

    if not password:
        return jsonify({"status": "error", "message": "Vui lòng nhập mật khẩu."})

    # Tạo MD5 của password nhập
    pas_md5 = hashlib.md5(password.encode('utf-8')).hexdigest()

    if pas_md5 != current_user.password:  # so sánh trực tiếp
        return jsonify({"status": "error", "message": "Mật khẩu bạn nhập không đúng."})

    return jsonify({"status": "success", "message": "Xác nhận thành công"})