from sqlalchemy import Column, String
from eapp.models import BaseModel
from sqlalchemy.orm import relationship


class Role(BaseModel):
    name = Column(String(50),nullable=False,unique=True)
    description = Column(String(200))

    accounts = relationship('Account',backref='role',lazy=True)
    # account_customers = relationship('Account', backref='customer', foreign_keys='Account.customer_id', lazy=True)
    # account_cashiers = relationship('Account', backref='cashier', foreign_keys='Account.cashier_id', lazy=True)
    # account_cashiers = relationship('Account', backref='staff', foreign_keys='Account.staff_id', lazy=True)

