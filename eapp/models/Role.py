from sqlalchemy import Column, String
from eapp.models import BaseModel


class Role(BaseModel):
    name = Column(String(50),nullable=False,unique=True)
    description = Column(String(200))
    