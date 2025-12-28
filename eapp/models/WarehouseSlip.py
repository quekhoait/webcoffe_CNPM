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
    stock_user_id = Column(ForeignKey('account.id'))
    invoice_id = Column(ForeignKey('invoice.id'))

    source_warehouse = relationship(
        "Warehouse",
        foreign_keys=[source_warehouse_id],
        backref="source_slips"
    )

    destination_warehouse = relationship(
        "Warehouse",
        foreign_keys=[destination_warehouse_id],
        backref="destination_slips"
    )
    slip_details = relationship('WarehouseSlipDetail',backref='warehouse_slip',lazy=True)
    __table_args__ = (UniqueConstraint('invoice_id'),)
    serialize_rules = ('-destination_warehouse','-source_warehouse',)
    # invoice
    