from eapp.models import Invoice
from eapp import db
import uuid

def generate_order_code():
    return f"DHCF_{uuid.uuid4().hex[:10]}"

def create_Invoice_dao( user_id,
    subtotal,
    extra_fee_total,
    total,
    payment_method,
    note):
    invoice=Invoice(
        order_code=generate_order_code(),
        customer_id=user_id,
        # subtotal=subtotal,
        # extra_fee_total=extra_fee_total,
        # final_total=subtotal + extra_fee_total,
        final_total=total,
        payment_method=payment_method,
        note=note
    )
    db.session.add(invoice)
    db.session.commit()
    return invoice