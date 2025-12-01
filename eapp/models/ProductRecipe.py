from sqlalchemy import Column, Float, ForeignKey, UniqueConstraint

from eapp.models import BaseModel


class ProductRecipe(BaseModel):

    product_id = Column(ForeignKey('product.id'), nullable=False)
    ingredient_id = Column(ForeignKey('ingredient.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(Float, nullable=False)

    
    __table_args__ = (UniqueConstraint('product_id', 'ingredient_id'),)

    