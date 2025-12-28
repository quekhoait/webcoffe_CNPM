from sre_constants import IN
from flask import jsonify, render_template, request, session

from eapp.dao import RuleDAO
from eapp.dao.InvoiceDAO import InvoiceDAO, InvoiceFilter
from eapp.models import Account
from eapp.models.Invoice import INVOICE_STATUS_LABEL, InvoiceStatusEnum
from eapp.models.Rule import Rule, RuleType
from eapp.services.InvoiceService import InvoiceService
from flask_login import login_user, logout_user, current_user, login_required

from eapp.services.RuleService import RuleService


def load_cashier():
    user = current_user
    invoices = InvoiceDAO.list(InvoiceFilter(payment_method="CASH"))
    invoice = invoices[0]
    rules = RuleDAO.list(RuleDAO.RuleFilter(rule_type=RuleType.SERVICE))
    payment_method = 'CASH'
    return render_template('cashier/cashier.html',
                           user=user,
                           invoices = invoices,
                           INVOICE_STATUS_LABEL=INVOICE_STATUS_LABEL,
                           payment_method=payment_method,
                           invoice=invoice,
                           warehouse_id = session.get('warehouse_id',1),
                           rules=rules)

def load_status_bar():
    data = request.args.to_dict()

    return render_template('cashier/cashier_invoice_status.html',
                           payment_method=data['payment_method'],
                           INVOICE_STATUS_LABEL=INVOICE_STATUS_LABEL)


#API INVOICE
def load_invoices():
    data = request.args.to_dict()
    filter = InvoiceFilter(**data)
    invoices = InvoiceDAO.list(filter)
    return render_template('cashier/cashier_invoice_item.html',
                           invoices=invoices,
                           INVOICE_STATUS_LABEL=INVOICE_STATUS_LABEL,
                           payment_method=data['payment_method'])

def update_invoice_status():
    params = request.json
    invoice = InvoiceDAO.get_by_id(params['invoice_id'])
    invoice_status = InvoiceStatusEnum[params['invoice_status']]
    invoice.cashier_id = current_user.id
    warehouse_id = get_current_warehouse_id()
    result = InvoiceService.update_invoice_status(invoice=invoice,new_status=invoice_status,warehouse_id=warehouse_id)
    # result['invoice'] = result['invoice'].to_dict() if result['invoice'] else None
    return jsonify({
        'success' : result['success'],
        'message' : result['message']
    })

def load_invoice_detail():
    invoice_id = request.args.get('invoice_id')
    invoice = InvoiceDAO.get_by_id(invoice_id)
    
    rules = RuleDAO.list(RuleDAO.RuleFilter(rule_type=RuleType.SERVICE))

    return render_template('cashier/invoice_detail.html',
                           invoice=invoice,
                           rules=rules)


def get_current_warehouse_id():
    return RuleService.get_rule_warehouse_id()