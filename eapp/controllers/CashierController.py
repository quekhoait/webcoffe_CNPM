from sre_constants import IN
from flask import render_template, request

from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.models import Account
from eapp.models.Invoice import INVOICE_STATUS_LABEL


def load_cashier():
    user = get_current_user()
    invoice = InvoiceDAO.get_by_id(10)
    invoices = InvoiceDAO.list()
    invoice_type = 'offline'
    return render_template('cashier/cashier.html',
                           user=user,
                           invoices = invoices,
                           INVOICE_STATUS_LABEL=INVOICE_STATUS_LABEL,
                           invoice_type=invoice_type,
                           invoice=invoice)

def load_status_bar():
    data = request.args.to_dict()

    return render_template('cashier/cashier_invoice_status.html',
                           invoice_type=data['invoice_type'],
                           INVOICE_STATUS_LABEL=INVOICE_STATUS_LABEL)


#API INVOICE
def load_invoices():
    data = request.args.to_dict()

    invoices = InvoiceDAO.list(params=data)
    return render_template('cashier/cashier_invoice_item.html',
                           invoices=invoices,
                           INVOICE_STATUS_LABEL=INVOICE_STATUS_LABEL,
                           invoice_type=data['invoice_type'])

def load_invoice_detail():
    invoice_id = request.args.get('invoice_id')
    invoice = InvoiceDAO.get_by_id(invoice_id)

    return render_template('cashier/invoice_detail.html',
                           invoice=invoice)

def get_current_user():
    return Account.query.get(1)