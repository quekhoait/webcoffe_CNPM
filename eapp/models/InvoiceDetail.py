from sqlalchemy import Column, Float, ForeignKey, Integer, UniqueConstraint
from eapp.models import BaseModel


class InvoiceDetail(BaseModel):
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    invoice_id = Column(ForeignKey('invoice.id'), nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    __table_args__ = (UniqueConstraint('invoice_id', 'product_id'),)
    
