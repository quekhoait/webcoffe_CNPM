from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from eapp.models.BaseModel import BaseModel
from eapp.models.Product import Dish


class Order(BaseModel):
    __tablename__ = 'HoaDon'

    id = Column('idHoaDon', Integer, primary_key=True)
    created_date = Column('NgayLap', DateTime, default=datetime.now)
    total_amount = Column('TongThanhToan', Float, default=0)
    payment_method = Column('HinhThucThanhToan', String(50))

    #người dùng đã đăng nhập
    user_id = Column('NguoiDung_idKhachHang', Integer, ForeignKey('NguoiDung.idNguoiDung'), nullable=False)

    receiver_name = Column('TenNguoiNhan', String(100))
    receiver_phone = Column('SDTNguoiNhan', String(20))
    note = Column('GhiChu', String(255))

    details = relationship('OrderDetail', backref='order', lazy=True)


class OrderDetail(BaseModel):
    __tablename__ = 'ChiTietHoaDon'

    id = Column('idChiTietHoaDon', Integer, primary_key=True)
    quantity = Column('SoLuong', Integer, default=1)
    price = Column('DonGia', Float)
    total_price = Column('ThanhTien', Float)

    order_id = Column('HoaDon_idHoaDon', Integer, ForeignKey('HoaDon.idHoaDon'), nullable=False)
    dish_id = Column('Mon_idMon', Integer, ForeignKey('Mon.idMon'), nullable=False)  # Lưu ý tên bảng Mon

    dish = relationship(Dish, backref='order_details')