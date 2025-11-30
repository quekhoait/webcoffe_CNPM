from eapp.models import Account
import hashlib
from eapp import db, app

def add_account(username, phone, name, password):
  newUser=Account(username=username,
                  phone=phone,
                  name=name,
                  password=str(hashlib.md5(password.strip().encode('utf-8')).hexdigest()))
  db.session.add(newUser)
  db.session.commit()