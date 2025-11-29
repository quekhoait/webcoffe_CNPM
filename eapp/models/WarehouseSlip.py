import enum

from sqlalchemy import Column, Enum as SqlEnum, ForeignKey, String
from eapp.models import BaseModel

class SlipType(enum.Enum):
    IMPORT = "IMPORT"
    EXPORT = "EXPORT"
    UPDATE = "UPDATE"

class WarehouseSlip(BaseModel):
    updated_date = None
    slip_type = Column(SqlEnum(SlipType),nullable=False)
    note = Column(String(200))
    source_warehouse_id = Column(ForeignKey('warehouse.id'))
    destination_warehouse_id = Column(ForeignKey('warehouse.id'))
    stock_user_id = Column(ForeignKey('account.id'),nullable=False)
    



