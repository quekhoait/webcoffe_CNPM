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

