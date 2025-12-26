from sqlalchemy import Column, Float, ForeignKey, String, UniqueConstraint

from eapp.models import BaseModel
from sqlalchemy.orm import relationship

class ProductRecipe(BaseModel):

    product_id = Column(ForeignKey('product.id'), nullable=False)
    ingredient_id = Column(ForeignKey('ingredient.id'), nullable=False)
    quantity = Column(Float, nullable=False)
    # unit = Column(String(20), nullable=False)


    serialize_rules = ('-product', '-ingredient.product_recipes', '-ingredient.stocks')

    
    __table_args__ = (UniqueConstraint('product_id', 'ingredient_id'),)

    