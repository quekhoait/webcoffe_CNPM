from sqlalchemy import or_
from eapp.models.Account import Account
import hashlib
from eapp import db, app
from eapp.models.Account import Role

def check_phone_exists(phone):
    return Account.query.filter_by(phone=phone).first() is not None

def add_account(username, phone, name, password):
  newUser=Account(username=username,
                  phone=phone,
                  name=name,
                  password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()))
  db.session.add(newUser)
  db.session.commit()

def login_account(identifier, password):
    password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Account.query.filter(or_(Account.phone == identifier.strip(), Account.username == identifier.strip()),
                                 Account.password==password).first()

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
    #lấy tất cả acc mà k phải là user
    return Account.query.filter(Account.role != Role.USER).all()

def get_account_by_id(user_id):
    return Account.query.get(user_id)

def create_employee(name, phone, email, password, role_enum, address=None):

    hashed_pass = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    new_acc = Account(
        name=name,
        phone=phone,
        username=phone,
        email=email,
        password=hashed_pass,
        role=role_enum,
        address=address,
        status=True,
        provider='local'
    )
    db.session.add(new_acc)
    db.session.commit()
    return new_acc


def update_employee_info(user_id, name, phone, email, role_enum, address, status, password=None):
    user = Account.query.get(user_id)
    if not user:
        return False

    user.name = name
    user.phone = phone
    user.username = phone
    user.email = email
    user.role = role_enum
    user.address = address
    user.status = status

    #có nhập pass mới thì đổi
    if password:
        user.password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    db.session.commit()
    return True


def delete_employee_dao(user_id):

    user = Account.query.get(user_id)
    if user:
        #xóa vĩnh viễn thì sẽ lỗi khóa ngoại đã có hóa đơn
        # db.session.delete(user)

        #khóa tài khoản
        user.status = False

        db.session.commit()
        return True
    return False