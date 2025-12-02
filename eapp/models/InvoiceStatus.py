import re
from sqlalchemy import Column, String
from eapp.models import BaseModel
from sqlalchemy.orm import relationship


class InvoiceStatus(BaseModel):
    name = Column(String(50), nullable=False)
    code = Column(String(20), nullable=False, unique=True)
    description = Column(String(200))
    created_date = None
    updated_date = None
    invoices = relationship('Invoice', backref='invoice_status', lazy=True)
