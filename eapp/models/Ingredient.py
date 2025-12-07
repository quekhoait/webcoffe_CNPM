from sqlalchemy import Column, Float, String
from eapp.models import BaseModel
from sqlalchemy.orm import relationship

class Ingredient(BaseModel):
    name = Column(String(100), nullable=False)
    unit = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(200), nullable=True)

    products = relationship('ProductRecipe', backref='ingredient', lazy=True)
    
    def __str__(self):
        return self.name
