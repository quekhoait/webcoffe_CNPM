# #Model chung
#
# # Import đối tượng db từ eapp/__init__.py
from flask_sqlalchemy import SQLAlchemy
from eapp import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime



class BaseModel(db.Model, SerializerMixin):
    __abstract__ = True
#
    # Định nghĩa các cột chung
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
#
#     def __repr__(self):
#         # Hàm hiển thị thông tin đối tượng khi debug
#         return f"<{self.__class__.__name__} {self.id}>"
