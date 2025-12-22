from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy import and_, exists, or_
from eapp import app, db
from eapp.models.Account import Account
from eapp.models.Invoice import Invoice, PaymentMethod
from eapp.models.InvoiceDetail import InvoiceDetail

@dataclass
class InvoiceFilter:
    payment_method : Optional[str] = None
    keyword : Optional[str] = None
    date : Optional[str] = None
    invoice_status : Optional[str] = None
    # order_code : Optional[str] = None
class InvoiceDAO:
    @staticmethod
    def list(params: InvoiceFilter = None):
        try:
            query = Invoice.query
            if params:
                if params.payment_method == 'CASH':
                    query = query.filter(Invoice.payment_method.__eq__(PaymentMethod.CASH))
                elif params.payment_method == 'MOMO':
                    query = query.filter(Invoice.payment_method.__eq__(PaymentMethod.MOMO))

                if params.keyword:
                    kw = f"%{params.keyword}%"
                    query = query.filter(or_(
                        Invoice.order_code.ilike(kw),
                        exists().where(
                            Account.id.in_([Invoice.customer_id,Invoice.staff_id,Invoice.cashier_id])
                        ).where(Account.name.ilike(kw))
                    ))
                
                if params.invoice_status:
                    query = query.filter(Invoice.invoice_status.__eq__(params.invoice_status))

                if params.date:
                    start = datetime.strptime(params.date,'%Y-%m-%d')
                    end = start + timedelta(days=1)
                    query = query.filter(
                        and_(Invoice.created_date >= start,
                             Invoice.created_date < end)
                    )
                
        except Exception as ex:
            app.logger.error(f"Lỗi khi lấy danh sách invoice: {ex}")
            return []
        return query.all()
    

    @staticmethod
    def create(data: dict) -> Invoice:
        try:
            invoice = Invoice(**data)
            db.session.add(invoice)
            db.session.commit()
            return invoice
        except Exception as ex:
            print(f"Lỗi khi tạo invoice: {ex}")
            return None
        
    @staticmethod
    def create(invoice: Invoice, invoice_details: list) -> Invoice:
        db.session.add(invoice)
        db.session.flush()   

        for detail in invoice_details:
            detail.invoice_id = invoice.id

        db.session.add_all(invoice_details)
        db.session.flush()

        return invoice

    @staticmethod
    def get_by_id(invoice_id: int) -> Invoice:
        try:
            invoice = Invoice.query.get(invoice_id)
            return invoice
        except Exception as ex:
            print(f"Lỗi khi lấy invoice theo id: {ex}")
            return None
    
    @staticmethod
    def save(invoice: Invoice):
        db.session.add(invoice)

    @staticmethod
    def save_details(details: list):
        db.session.add_all(details)
    
