from enum import Enum

from sqlalchemy import Column, String, Float, Enum as SQLEnum, Integer, ForeignKey, DateTime

from eapp.models.BaseModel import BaseModel
from eapp.models.Category import DishCategory


class DishStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

# class Dish(BaseModel):
#     name = Column(String(100), nullable=False)
#     unit = Column(String(20), nullable=True)
#     price = Column(Float)
#     status = Column(SQLEnum(DishStatus),default=DishStatus.ACTIVE, nullable=False)
#     description = Column(String(200))
#     image = Column(String(200))
#     rating_score = Column(Float, default=5)
#     rating_count = Column(Integer, default=0)
#
#     dish_category_id = Column(Integer, ForeignKey(DishCategory.id), nullable=False)
#
#     def __str__(self):
#         return self.name



class Dish(BaseModel):
    __tablename__ = 'Mon'

    id = Column('idMon', Integer, primary_key=True)

    name = Column('TenMon', String(100), nullable=False)
    unit = Column('DonVi', String(20))
    price = Column('DonGia', Float)
    status = Column('TrangThai', String(50), default="Còn hàng")
    description = Column('MoTa', String(200))
    image = Column('HinhAnh', String(200))

    created_date = Column('NgayTao', DateTime)
    rating_count = Column('SoLuotDanhGia', Integer, default=0)

    dish_category_id = Column('DanhMucMon_idDanhMucMon', Integer, ForeignKey('DanhMucMon.idDanhMucMon'), nullable=False)

    def __str__(self):
        return self.name