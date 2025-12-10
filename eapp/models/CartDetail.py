from eapp.models.BaseModel import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Float, String, Enum as SqlEnum, ForeignKey


from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from eapp.models.BaseModel import BaseModel


class CartDetail(BaseModel):
    cart_id = Column(Integer, ForeignKey("cart.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Integer)          # giá đơn
    total_price = Column(Integer)         # thành tiền
    note = Column(String(255))

    # Quan hệ
    product = relationship("Product", backref="cart_details", lazy=True)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"

