import re
from sqlalchemy import Column, Float, ForeignKey, String
from eapp.models import BaseModel
from sqlalchemy.orm import relationship


class Invoice(BaseModel):
    cashier_id = Column(ForeignKey('account.id'), nullable=False)
    customer_id = Column(ForeignKey('account.id'))
    staff_id = Column(ForeignKey('account.id'), nullable=False)
    total_amount = Column(Float, nullable=False)
    updated_date = None
    subtotal = Column(Float, nullable=False)
    extra_fee_total = Column(Float, nullable=False)
    final_total = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)
    invoice_status_id = Column(ForeignKey('invoice_status.id'), nullable=False)
    invoice_details = relationship('InvoiceDetail', backref='invoice', lazy=True)
    