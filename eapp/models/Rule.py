from enum import Enum
from sqlalchemy import Boolean, Column, Float, Integer, String, Enum as SqlEnum
from eapp.models import BaseModel

class RuleType(Enum):
    SERVICE = "service"
    INGREDIENT = "ingredient"

class Rule(BaseModel):
    name = Column(String(100), nullable=False, unique=True)
    rule_type = Column(SqlEnum(RuleType), nullable=False)
    value = Column(Float)
    unit = Column(String(50))
    instance_rule_id = Column(Integer)
    description = Column(String(200))
    active = Column(Boolean, default=True)

