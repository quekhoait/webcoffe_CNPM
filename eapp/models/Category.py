from sqlalchemy import Column, String

from eapp.models.BaseModel import BaseModel
from sqlalchemy.orm import relationship


class Category(BaseModel):
    name = Column(String(100),nullable=False)
    description = Column(String(200))
    products = relationship('Product', backref='category', lazy=True)
    def __str__(self):
        return self.name

