from sqlalchemy import Column, String

from eapp.models.BaseModel import BaseModel


class DishCategory(BaseModel):
    name = Column(String(100),nullable=False)
    description = Column(String(200))

    def __str__(self):
        return self.name
