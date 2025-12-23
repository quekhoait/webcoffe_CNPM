
from flask import jsonify, redirect, render_template, request, url_for

from eapp.dao import RuleDAO
from eapp.models.Rule import Rule, RuleType


def index():
    rules = RuleDAO.list()
    rule_types = RuleType
    if request.method == 'POST':
        name = request.form.get("name")
        value = request.form.get("value")
        rule_type = request.form.get("rule_type")
        unit = request.form.get("unit")
        description = request.form.get("description")
        active = request.form.get('active')
        rule = Rule(
            name=name,
            value=value,
            rule_type=RuleType[rule_type],
            unit=unit,
            description=description,
            active=int(active)
        )
        RuleDAO.create(rule)
        return redirect(url_for('rule'))

    return render_template('rule/rule.html',
                        rules=rules,
                        rule_types=rule_types)


def delete_rule(rule_id):
    RuleDAO.delete(rule_id)
    return ""


def update_rule(rule_id):
    data = {
        "name": request.form.get("name"),
        "value": request.form.get("value"),
        "rule_type": request.form.get("rule_type"),
        "unit": request.form.get("unit"),
        "description": request.form.get("description"),
        "active": request.form.get("active")
    }

    rule = RuleDAO.update(rule_id, data)

    if not rule:
        return jsonify({"message": "Rule không tồn tại"})

    return redirect(url_for("rule"))