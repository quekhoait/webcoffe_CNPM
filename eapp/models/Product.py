from enum import Enum

from sqlalchemy import Column, String, Float, Enum as SQLEnum, Integer, ForeignKey

from eapp.models.BaseModel import BaseModel
from eapp.models.Category import Category
from sqlalchemy.orm import relationship


class ProductStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class Product(BaseModel):
    name = Column(String(100), nullable=False)
    unit = Column(String(20), nullable=True)
    price = Column(Float)
    status = Column(SQLEnum(ProductStatus),default=ProductStatus.ACTIVE, nullable=False)
    description = Column(String(200))
    image = Column(String(200))
    rating_score = Column(Float, default=5)
    rating_count = Column(Integer, default=0)
    dish_category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    ingredients = relationship('ProductRecipe', backref='product', lazy=True)
    def __str__(self):
        return self.name