from sqlalchemy import Column, String
from eapp.models import BaseModel
from sqlalchemy.orm import relationship


class Warehouse(BaseModel):
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=True)

    stocks = relationship("Stock", backref="warehouse", lazy=True)
    def __str__(self):
        return self.name