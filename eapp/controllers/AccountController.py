from flask import render_template, request, redirect, jsonify, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from eapp import app, utils
import math, re, hashlib, cloudinary.uploader
from eapp.dao.AccountDAO import add_account, check_phone_exists, login_account, update_account_dao
from werkzeug.security import check_password_hash
from eapp.models.Account import Role


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
    identifier = request.form.get("phone")
    password = request.form.get("password")
    # phone_regex = r"^0\d{9}$"
    if not identifier or not password:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ giá trị!"})
    # if not re.match(phone_regex, identifier):
    #     return jsonify({"status": "error", "message": "Số điện thoại không hợp lệ!"})
    if len(password) < 6:
        return jsonify({"status": "error", "message": "Mật khẩu phải hơn 6 ký tự!"})
    try:
        u = login_account(identifier=identifier, password=password)
        if not u:
            return jsonify({"status": "error", "message": "Sai số điện thoại/username hoặc mật khẩu!"})

        # login_user là của flask_login
        login_user(u)
        print(u.role)

        if u.role== Role.USER:
            redirect_url = url_for("index")
        elif u.role == Role.STAFF:
            redirect_url = url_for("staff")
        elif u.role == Role.CASHIER:
            redirect_url = url_for('cashier')
        elif u.role == Role.WAREHOUSE_KEEPER:
            redirect_url = url_for("warehouse")
        # elif u.role == Role.ADMIN:
        #     return redirect(url_for("user"))
        return jsonify({"status": "success", "message": "Đăng nhập thành công!", "redirect_url": redirect_url})
    except Exception as ex:
        app.logger.error(f'Lỗi khi đăng nhập: {ex}')
        print(ex)
        return jsonify({"status": "error", "message": "Có lỗi xảy ra, thử lại sau!"})

def logout():
    logout_user()
    return redirect('/login')

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


def update_account():
    user_id = request.form.get("id")
    username = request.form.get("username")
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    password = request.form.get("password")
    address = request.form.get("address")
    avatar=request.files.get("avatar")
    phone_regex = r"^0\d{9}$"
    if avatar and avatar.filename != '':
        res = cloudinary.uploader.upload(
            avatar,
            folder=f"users/{user_id}"
        )
        avatar_url = res.get('secure_url')
    else:
        avatar_url = current_user.avatar
    if not username or not phone or not name or not password:
        return jsonify({"status": "error", "message": "Vui lòng nhập đầy đủ giá trị!"})
    if not re.match(phone_regex, phone):
        return jsonify({"status": "error", "message": "Số điện thoại không hợp lệ!"})
    if password != "******" and len(password) < 6:
        return jsonify({"status": "error", "message": "Mật khẩu phải hơn 6 ký tự!"})
    try:
        updated_user = update_account_dao(
            user_id=user_id,
            username=username,
            phone=phone,
            name=name,
            password=password,
            email=email,
            address=address,
            avatar=avatar_url
        )
        if updated_user is None:
            return jsonify({"status": "error", "message": "Không thể cập nhật tài khoản!"})

        return jsonify({"status": "success", "message": "Cập nhật thành công!"})

    except Exception as ex:
        app.logger.error(f"Lỗi khi cập nhật tài khoản: {ex}")
        return jsonify({"status": "error", "message": "Có lỗi xảy ra, thử lại sau!"})
