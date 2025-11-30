from sqlalchemy import Column, String, Boolean, DateTime
from eapp.models.BaseModel import BaseModel
from datetime import datetime

class Account(BaseModel):
    __tablename__ = 'accounts'
    username = Column(String(100), nullable=False, unique=True)
    phone = Column(String(25), nullable=False, unique=True) 
    name = Column(String(100))
    password = Column(String(255), nullable=False)    
    email = Column(String(100), unique=True) 
    provider = Column(String(50), default='local')
    avatar=Column(String(250))
    status=Column(Boolean)

    def __str__(self):
        return f"Account(ID: {self.id}, Username: {self.username})"