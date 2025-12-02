from enum import Enum
import re
from sqlalchemy import Column, Float, ForeignKey, String, Enum as SqlEnum
from eapp.models import BaseModel
from sqlalchemy.orm import relationship

class PaymentMethod(Enum):
    CASH = 'Tiền mặt'
    BANK_TRANSFER = 'Chuyển khoản'
    OTHER = 'Khác'

class Invoice(BaseModel):
    cashier_id = Column(ForeignKey('account.id'), nullable=True)
    customer_id = Column(ForeignKey('account.id'))
    staff_id = Column(ForeignKey('account.id'), nullable=True)
    subtotal = Column(Float, nullable=False)
    extra_fee_total = Column(Float, nullable=False)
    final_total = Column(Float, nullable=False)
    payment_method = Column(SqlEnum(PaymentMethod), nullable=False)
    invoice_status_id = Column(ForeignKey('invoice_status.id'), nullable=False)
    invoice_details = relationship('InvoiceDetail', backref='invoice', lazy=True)
    