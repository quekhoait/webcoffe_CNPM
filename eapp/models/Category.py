from sqlalchemy import Column, String, Integer

from eapp.models.BaseModel import BaseModel


# class DishCategory(BaseModel):
#     name = Column(String(100),nullable=False)
#     description = Column(String(200))
#
#     def __str__(self):
#         return self.name


class DishCategory(BaseModel):
    __tablename__ = 'DanhMucMon'

    id = Column('idDanhMucMon', Integer, primary_key=True)
    name = Column('TenDanhMucMon', String(100), nullable=False)
    description = Column('MoTa', String(200))

    def __str__(self):
        return self.name