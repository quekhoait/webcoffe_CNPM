from enum import Enum
from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String, Enum as SqlEnum
from eapp.models import BaseModel

class RuleType(Enum):
    SERVICE = "Phí phục vụ"
    INGREDIENT = "Tồn nguyên liệu"

class Rule(BaseModel):
    name = Column(String(100), nullable=False, unique=True)
    rule_type = Column(SqlEnum(RuleType), nullable=False)
    value = Column(Float)
    unit = Column(String(50))
    description = Column(String(200))
    active = Column(Boolean, default=True)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
