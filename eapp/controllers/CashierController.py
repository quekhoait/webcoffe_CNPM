from flask import render_template

from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.models import Account


def load_cashier():
    user = get_current_user()
    invoices = InvoiceDAO.list()
   
    return render_template('cashier/cashier.html',
                           user=user,
                           invoices = invoices)

def get_current_user():
    return Account.query.get(1)