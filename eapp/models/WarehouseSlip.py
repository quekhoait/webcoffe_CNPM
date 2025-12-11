import enum

from sqlalchemy import Column, Enum as SqlEnum, ForeignKey, String, UniqueConstraint
from eapp.models import BaseModel
from sqlalchemy.orm import relationship
class SlipType(enum.Enum):
    IMPORT = "Nhập Kho"
    EXPORT = "Xuất Kho"
    UPDATE = "Cập Nhật Kho"
    TRANSFER = "Chuyển Kho"

class WarehouseSlip(BaseModel):
    updated_date = None
    slip_type = Column(SqlEnum(SlipType),nullable=False)
    note = Column(String(200))
    source_warehouse_id = Column(ForeignKey('warehouse.id'))
    destination_warehouse_id = Column(ForeignKey('warehouse.id'))
    stock_user_id = Column(ForeignKey('account.id'),nullable=False)
    invoice_id = Column(ForeignKey('invoice.id'))

    slip_details = relationship('WarehouseSlipDetail',backref='warehouse_slip',lazy=True)
    __table_args__ = (UniqueConstraint('invoice_id'),)
    # invoice
    