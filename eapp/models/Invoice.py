# from enum import Enum
import re
from enum import Enum
from sqlalchemy import Column, Float, String, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from eapp.models import BaseModel


class InvoiceStatusEnum(str, Enum):
    PENDING = "pending"  # Chờ xử lý / chờ phục vụ
    IN_PROGRESS = "in_progress"  # Đang giao / đang phục vụ
    COMPLETED = "completed"

class PaymentMethod(Enum):
    CASH = 'Tiền mặt'
    BANK_TRANSFER = 'Chuyển khoản'
    OTHER = 'Khác'

class Invoice(BaseModel):
    cashier_id = Column(ForeignKey('account.id'), nullable=True)
    customer_id = Column(ForeignKey('account.id'))
    staff_id = Column(ForeignKey('account.id'), nullable=False)
    subtotal = Column(Float, nullable=False)
    extra_fee_total = Column(Float, nullable=False)
    final_total = Column(Float, nullable=False)
    note = Column(String(255))
    payment_method = Column(String(50), nullable=False)
    invoice_status = Column(SqlEnum(InvoiceStatusEnum), nullable=False)
    
    invoice_details = relationship("InvoiceDetail", backref="invoice", lazy=True)
