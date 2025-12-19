from eapp.dao import InvoiceDAO
from eapp.models import Invoice, InvoiceDetail, Payment
from eapp.models.Payment import PaymentStatus
from eapp import db
from datetime import datetime, timedelta
import uuid



def generate_order_code():
    return f"DHCF_{uuid.uuid4().hex[:10]}"

def create_Invoice_dao( user_id,
    # subtotal,
    # extra_fee_total,
    total,
    payment_method,
    note):
    try:

        invoice = Invoice(
            order_code=generate_order_code(),
            customer_id=user_id,
            subtotal=9999999,
            extra_fee_total=9999,
            final_total=total,
            payment_method=payment_method,
            note=note
        )

        db.session.add(invoice)
        db.session.commit()
        return invoice
    except Exception as ex:
        print(f"Lỗi : {ex}")
        return []




def create_InvoiceDetail_dao(product_id, invoice_id, quantity, price):
    invoiceDetail = InvoiceDetail(
        invoice_id=invoice_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )
    db.session.add(invoiceDetail)
    db.session.commit()
    return invoiceDetail


def create_Payment_dao( invoice_id,amount):
    payment = Payment(
        invoice_id=invoice_id,
        amount=amount,
        status=PaymentStatus.pending,
        provider="momo",
        expired_date = datetime.now() + timedelta(minutes=100)
    )
    db.session.add(payment)
    db.session.commit()
    return payment

def get_by_momo_id(momo_id):
    return Payment.query.filter_by(momo_id=momo_id).first()

def repay_payment_dao(invoice_id):
    payment = Payment.query.filter(
        Payment.invoice_id == invoice_id,
        Payment.status == PaymentStatus.pending,
        Payment.expired_date > datetime.now()
        ).order_by(Payment.created_date.desc()).first() #sắp xếp lấy cái mới nhất
    invoice=Invoice.query.get(invoice_id)
    amount=invoice.final_total
    if payment:
        return payment
    newPayment=create_Payment_dao(invoice_id, amount)
    return newPayment