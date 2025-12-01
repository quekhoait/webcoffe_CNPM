from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean
from eapp.models.BaseModel import BaseModel

class Account(BaseModel, UserMixin):
    __tablename__ = 'accounts'
    username = Column(String(100), nullable=False, unique=True)
    phone = Column(String(25), nullable=False, unique=True)
    name = Column(String(100))
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    address=Column(String(255))
    provider = Column(String(50), default='local')
    avatar=Column(String(250))
    status=Column(Boolean, default=True)

    def __str__(self):
        return f"Account(ID: {self.id}, Username: {self.username})"
