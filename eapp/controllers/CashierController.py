from flask import render_template

from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.dao.InvoiceStatusDAO import InvoiceStatusDAO
from eapp.models import Account


def load_cashier():
    user = get_current_user()
    invoice_status = InvoiceStatusDAO.list()
    invoices = InvoiceDAO.list()
    return render_template('cashier/cashier.html',
                           user=user,
                           invoice_status = invoice_status,
                           invoices = invoices)

def get_current_user():
    return Account.query.get(1)