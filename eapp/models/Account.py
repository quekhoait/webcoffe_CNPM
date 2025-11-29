from sqlalchemy import Column, ForeignKey, String
from eapp.models.BaseModel import BaseModel

class Account(BaseModel):
    username = Column(String(100), nullable=False, unique=True)
    phone = Column(String(25), nullable=False, unique=True) 
    name = Column(String(100))
    password = Column(String(255), nullable=False)    
    email = Column(String(100), unique=True) 
    provider = Column(String(50), default='local')
    role_id = Column(ForeignKey('role.id'), nullable=False)

    def __str__(self):
        return f"Account(ID: {self.id}, Username: {self.username})"