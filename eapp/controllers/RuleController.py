
from flask import jsonify, redirect, render_template, request, url_for
from flask_login import current_user

from eapp.dao import RuleDAO
from eapp.models.Rule import Rule, RuleType


def load_rule():
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
            account_id=current_user.id,
            name=name,
            value=value,
            rule_type=RuleType[rule_type],
            unit=unit,
            description=description,
            active=int(active)
        )
        RuleDAO.create(rule)
        return redirect(url_for('rule'))

    return render_template('admin/rule.html',
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


def get_rule():
    rule_quantity_invoice = RuleDAO.list(RuleDAO.RuleFilter(rule_type=RuleType.INVOICE))[0].value
    return jsonify({
        "rule_quantity": rule_quantity_invoice
    })
