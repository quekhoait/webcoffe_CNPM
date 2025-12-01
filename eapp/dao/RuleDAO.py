from eapp.models import Rule


def list(params: dict = None):
    try:
        query = Rule.query

        if params:
            if 'rule_type' in params:
                query = query.filter(Rule.rule_type == params['rule_type'])
        return query.all()
    except Exception as ex:
        print(f"Lỗi khi lấy danh sách rule: {ex}")
        return []
    
