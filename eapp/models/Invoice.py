import re
from enum import Enum
from sqlalchemy import Column, Float, String, Enum as SqlEnum, ForeignKey
from sqlalchemy.orm import relationship
from eapp.models import BaseModel


class InvoiceStatusEnum(str, Enum):
    PENDING_PAYMENT = "pending_payment"
    PENDING_PROCESSING = "pending_processing"
    SHIPPING = "shipping"
    DELIVERED = "delivered"


class Invoice(BaseModel):
    cashier_id = Column(ForeignKey('account.id'), nullable=False)
    customer_id = Column(ForeignKey('account.id'))
    staff_id = Column(ForeignKey('account.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    extra_fee_total = Column(Float, nullable=False)
    final_total = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    invoice_status = Column(SqlEnum(InvoiceStatusEnum), nullable=False)
    invoice_details = relationship("InvoiceDetail", backref="invoice", lazy=True)
