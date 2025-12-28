from dataclasses import dataclass
from typing import Optional
from eapp import app,db
from eapp.models.Rule import Rule, RuleType

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
    
def create(rule: Rule):
    try:
        db.session.add(rule)
        db.session.commit()
    except Exception as ex:
        app.logger.error(f"Lỗi khi lưu quy dịnh {str(ex)}", exc_info=True) 
        db.session.rollback()
        raise

def delete(rule_id):
    try:
        rule = Rule.query.get(rule_id)
        if not rule:
            return False

        db.session.delete(rule)
        db.session.commit()
        return True

    except Exception as ex:
        db.session.rollback() 
        app.logger.error(f"Lỗi khi xóa rule: {ex}", exc_info=True)
        raise

def update(rule_id: int, data: dict):
    try:
        rule = Rule.query.get(rule_id)
        if not rule:
            return None

        rule.name = data.get("name", rule.name)
        rule.value = data.get("value", rule.value)
        rule.rule_type = RuleType[data["rule_type"]] if "rule_type" in data else rule.rule_type
        rule.unit = data.get("unit", rule.unit)
        rule.description = data.get("description", rule.description)
        rule.active = int(data.get("active", rule.active))

        db.session.commit()
        return rule

    except Exception as ex:
        db.session.rollback()
        app.logger.error(f"Lỗi khi update rule: {ex}", exc_info=True)
        raise

