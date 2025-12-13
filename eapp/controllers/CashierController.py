from flask import render_template

from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.models import Account
from eapp.models.Invoice import INVOICE_STATUS_LABEL


def load_cashier():
    user = get_current_user()
    invoices = InvoiceDAO.list()
    invoice_type = 'online'
    return render_template('cashier/cashier.html',
                           user=user,
                           invoices = invoices,
                           INVOICE_STATUS_LABEL=INVOICE_STATUS_LABEL,
                           invoice_type=invoice_type)


#API INVOICE
def load_invoices():
    pass

def get_current_user():
    return Account.query.get(1)