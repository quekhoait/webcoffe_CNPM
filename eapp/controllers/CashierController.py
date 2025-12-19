from sre_constants import IN
from flask import jsonify, render_template, request, session

from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.models import Account
from eapp.models.Invoice import INVOICE_STATUS_LABEL, InvoiceStatusEnum
from eapp.services.InvoiceService import InvoiceService
from flask_login import login_user, logout_user, current_user, login_required


def load_cashier():
    user = current_user
    invoice = InvoiceDAO.get_by_id(10)
    invoices = InvoiceDAO.list()
    invoice_type = 'offline'
    return render_template('cashier/cashier.html',
                           user=user,
                           invoices = invoices,
                           INVOICE_STATUS_LABEL=INVOICE_STATUS_LABEL,
                           invoice_type=invoice_type,
                           invoice=invoice,
                           warehouse_id = session.get('warehouse_id',1))

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

def update_invoice_status():
    params = request.json
    invoice = InvoiceDAO.get_by_id(params['invoice_id'])
    invoice_status = InvoiceStatusEnum[params['invoice_status']]
    warehouse_id = 1 #chưa biểt lấy ở đâu
    result = InvoiceService.update_invoice_status(invoice=invoice,new_status=invoice_status,warehouse_id=warehouse_id)
    # result['invoice'] = result['invoice'].to_dict() if result['invoice'] else None
    print(result)
    return jsonify({
        'success' : result['success'],
        'message' : result['message']
    })

def load_invoice_detail():
    invoice_id = request.args.get('invoice_id')
    invoice = InvoiceDAO.get_by_id(invoice_id)
    

    return render_template('cashier/invoice_detail.html',
                           invoice=invoice)

