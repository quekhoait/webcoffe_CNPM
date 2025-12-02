from sqlalchemy import Column, String
from eapp.models import BaseModel
from sqlalchemy.orm import relationship


class Role(BaseModel):
    name = Column(String(50),nullable=False,unique=True)
    description = Column(String(200))
    accounts = relationship('Account', backref='role', lazy=True)