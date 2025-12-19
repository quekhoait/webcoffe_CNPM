from sqlalchemy import Column, Float, String
from eapp.models import BaseModel
from sqlalchemy.orm import relationship

class Ingredient(BaseModel):
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(200), nullable=True)

    stocks = relationship('Stock', backref='ingredient', lazy=True)
    products = relationship('ProductRecipe', backref='ingredient', lazy=True)

    serialize_rules = ('-stocks', '-products')
    
    def __str__(self):
        return self.name
