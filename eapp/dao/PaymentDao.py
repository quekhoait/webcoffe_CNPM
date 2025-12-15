from eapp.models import Invoice, InvoiceDetail, Payment
from eapp import db
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
        print(user_id, total, payment_method, note)
        invoice = Invoice(
            order_code=generate_order_code(),
            customer_id=user_id,
            # subtotal=subtotal,
            # extra_fee_total=extra_fee_total,
            # final_total=subtotal + extra_fee_total,
            final_total=total,
            payment_method=payment_method,
            note=note
        )
        import pdb
        pdb.set_trace()
        print("invoice2", invoice)
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


def create_Payment_dao( invoice_id,amount, payment_method, status):
    payment = Payment(
        invoice_id=invoice_id,
        amount=amount,
        payment_method=payment_method,
        status=status
    )
    db.session.add(payment)
    db.session.commit()
    return payment