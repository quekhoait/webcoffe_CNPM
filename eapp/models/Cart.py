from eapp.models.BaseModel import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, String, Enum as SqlEnum, ForeignKey, UniqueConstraint


class Cart(BaseModel):
    user_id= Column(ForeignKey('account.id'),  nullable=False, unique=True)
    details = relationship("CartDetail", backref="cart", lazy=True)
    serialize_rules = ('-details.product',)


    __table_args__ = (UniqueConstraint('user_id'),)

    def __str__(self):
        return self.name

