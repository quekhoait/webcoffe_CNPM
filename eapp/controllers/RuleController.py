
from flask import render_template

from eapp.dao import RuleDAO


def index():
    rules = RuleDAO.list()
    return render_template('rule/rule.html',
                        rules=rules)