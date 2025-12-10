from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from eapp.models import BaseModel


class Stock(BaseModel):
    warehouse_id = Column(ForeignKey('warehouse.id'), nullable=False)
    ingredient_id = Column(ForeignKey('ingredient.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('warehouse_id', 'ingredient_id'),)