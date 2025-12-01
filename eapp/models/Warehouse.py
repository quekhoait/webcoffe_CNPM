from sqlalchemy import Column, String
from eapp.models import BaseModel


class Warehouse(BaseModel):
    name = Column(String(100), nullable=False)
    location = Column(String(200), nullable=True)

    def __str__(self):
        return self.name