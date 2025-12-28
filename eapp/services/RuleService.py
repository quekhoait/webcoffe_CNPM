from eapp.dao import RuleDAO
from eapp.models import Warehouse
from eapp.models.Rule import RuleType


class RuleService:


    @staticmethod
    def calulate_service_fee(total : float) -> float:
        rules = RuleDAO.list(RuleDAO.RuleFilter(rule_type = RuleType.SERVICE))
        fee = 0
        for rule in rules:
            if rule.unit == "%":
                fee += total * (rule.value / 100)
            else:
                fee += rule.value
        return fee
    

    @staticmethod
    def get_rule_warehouse_id():
        rule = RuleDAO.list(RuleDAO.RuleFilter(rule_type=RuleType.WAREHOUSE))[0]
        return int(rule.value)
    