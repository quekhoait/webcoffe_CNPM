from dataclasses import dataclass
from typing import Optional
from eapp import app
from eapp.models import Rule

@dataclass
class RuleFilter:
    rule_type : Optional[str] = None

def list(params: RuleFilter = None):
    try:
        query = Rule.query

        if params:
            if params.rule_type:
                query = query.filter(Rule.rule_type == params.rule_type)

        return query.all()
    except Exception as ex:
        app.logger.error(f"Lỗi khi lấy danh sách rule: {ex}")
        return []
    
