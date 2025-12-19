from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Enum, UniqueConstraint, DateTime
from eapp.models import BaseModel
from datetime import datetime
import enum


class PaymentStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class Payment(BaseModel):
    momo_id = Column(String(100), nullable=True, unique=True)
    momo_trans_id = Column(BigInteger, nullable=True)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    amount = Column(BigInteger, nullable=False)
    payUrl= Column(String(500), nullable=True)
    invoice_id = Column(ForeignKey("invoice.id"), nullable=False)
    provider = Column(String(50), nullable=False, default="momo")
    expired_date  = Column(DateTime, nullable=False)