from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean,Enum as SQLEnum
from sqlalchemy import Column, ForeignKey, String
from eapp.models.BaseModel import BaseModel
from sqlalchemy.orm import relationship
from enum import Enum

class Role(Enum):
    USER="Người Dùng"
    STAFF="Nhân Viên"
    CASHIER="Thu Ngân"
    WAREHOUSE_KEEPER="Thủ Kho"
    ADMIN="Quản lý"
class Account(BaseModel, UserMixin):
    username = Column(String(100), nullable=False, unique=True)
    phone = Column(String(25), nullable=False, unique=True)
    name = Column(String(100))
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=False)
    address=Column(String(255))
    provider = Column(String(50), default='local')
    avatar=Column(String(250), default='https://res.cloudinary.com/ds11ggie4/image/upload/v1764250180/user_liifdm.png')
    status=Column(Boolean, default=True)
    role = Column(SQLEnum(Role), nullable=False, default=Role.USER)

    invoice_of_customers = relationship('Invoice', backref='customer', foreign_keys='Invoice.customer_id', lazy=True)
    invoice_of_staffs = relationship('Invoice',backref='staff',foreign_keys='Invoice.staff_id',lazy=True)
    invoice_of_cashiers = relationship('Invoice',backref='cashier',foreign_keys='Invoice.cashier_id',lazy=True)

    serialize_rules = ('-invoice_of_customers', '-invoice_of_staffs','-invoice_of_cashiers')

    def __str__(self):
        return f"Account(ID: {self.id}, Username: {self.username})"