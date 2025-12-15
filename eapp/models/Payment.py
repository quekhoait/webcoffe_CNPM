from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Enum, UniqueConstraint
from eapp.models import BaseModel
import enum


class PaymentStatus(enum.Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class Payment(BaseModel):
    momo_id = Column(String(100), nullable=True, unique=True)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    amount = Column(BigInteger, nullable=False)
    invoice_id = Column(ForeignKey("invoice.id"), nullable=False)
