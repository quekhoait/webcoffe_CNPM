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
    CASH = "CASH"
    MOMO = "MOMO"
    BANK_TRANSFER = "BANK_TRANSFER"

class Invoice(BaseModel):
    order_code = Column(String(50), unique=True, nullable=False)
    cashier_id = Column(ForeignKey('account.id'), nullable=True)
    customer_id = Column(ForeignKey('account.id'))
    staff_id = Column(ForeignKey('account.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    extra_fee_total = Column(Float, nullable=False)
    final_total = Column(Float, nullable=False)
    note = Column(String(255))
    payment_method = Column( SqlEnum(PaymentMethod), nullable=False)
    invoice_status = Column(SqlEnum(InvoiceStatusEnum), nullable=False, default=InvoiceStatusEnum.PENDING)
    invoice_details = relationship("InvoiceDetail", backref="invoice", lazy=True)
