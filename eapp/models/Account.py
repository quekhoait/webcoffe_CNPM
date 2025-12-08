from flask_login import UserMixin
from sqlalchemy import Column, String, Boolean
from sqlalchemy import Column, ForeignKey, String
from eapp.models.BaseModel import BaseModel
from sqlalchemy.orm import relationship

class Account(BaseModel):
    username = Column(String(100), nullable=False, unique=True)
    phone = Column(String(25), nullable=False, unique=True)
    name = Column(String(100))
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=False)
    address=Column(String(255))
    provider = Column(String(50), default='local')
    avatar=Column(String(250), default='https://res.cloudinary.com/ds11ggie4/image/upload/v1764250180/user_liifdm.png')
    status=Column(Boolean, default=True)
    role_id = Column(ForeignKey('role.id'), nullable=False, default=1)

    invoice_of_customers = relationship('Invoice', backref='customer', foreign_keys='Invoice.customer_id', lazy=True)
    invoice_of_staffs = relationship('Invoice',backref='staff',foreign_keys='Invoice.staff_id',lazy=True)
    invoice_of_cashiers = relationship('Invoice',backref='cashier',foreign_keys='Invoice.cashier_id',lazy=True)


    def __str__(self):
        return f"Account(ID: {self.id}, Username: {self.username})"