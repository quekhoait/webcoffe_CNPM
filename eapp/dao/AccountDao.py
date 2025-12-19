from eapp.models.Account import Account
import hashlib
from eapp import db, app

def check_phone_exists(phone):
    return Account.query.filter_by(phone=phone).first() is not None

def add_account(username, phone, name, password):
  newUser=Account(username=username,
                  phone=phone,
                  name=name,
                  password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()))
  db.session.add(newUser)
  db.session.commit()

def login_account(phone, password):
    password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Account.query.filter(Account.phone==phone.strip(), Account.password==password).first()

def update_account_dao(user_id, username, phone, name, password, email, address, avatar):
    print(user_id)
    user = Account.query.get(user_id)
    if not user:
        return None
    # Kiểm tra số điện thoại trùng người khác
    acc = Account.query.filter_by(phone=phone).first()
    if acc and acc.id != int(user_id):
        return None
    # Xử lý password
    if password == "******":
        pas = user.password
    else:
        pas = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    # Cập nhật dữ liệu
    user.username = username
    user.phone = phone
    user.name = name
    user.password = pas
    user.email = email
    user.address = address
    user.avatar=avatar
    db.session.commit()
    return user



def get_all_employees():
    return Account.query.all()

def admin_create_account(data):
    return False

def admin_update_account(user_id, data):
    return False

def admin_delete_account(user_id):
    return False