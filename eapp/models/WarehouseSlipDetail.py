from sqlalchemy import Column, Float, ForeignKey, Integer, String, UniqueConstraint
from eapp.models import BaseModel


class WarehouseSlipDetail(BaseModel):
    created_date = None
    updated_date = None
    warehouse_slip_id = Column(ForeignKey('warehouse_slip.id'),nullable=False)
    ingredient_id = Column(ForeignKey('ingredient.id'),nullable=False)
    quantity = Column(Float,nullable=False)

    __table_args__ = (UniqueConstraint('warehouse_slip_id','ingredient_id'),)