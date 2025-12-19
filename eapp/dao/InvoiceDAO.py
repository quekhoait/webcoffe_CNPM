from eapp.models import Invoice
from eapp import app, db
from eapp.models.InvoiceDetail import InvoiceDetail
from eapp.services.InventoryService import InventoryService



class InvoiceDAO:
    @staticmethod
    def list(params: dict = None):
        try:
            query = Invoice.query
            if params:
                if params['invoice_type'] == 'offline': #tại quầy
                    query = query.filter(Invoice.customer_id == None)
                else: # online
                    query = query.filter(Invoice.staff_id == None)
                if params.get('invoice_status'):
                    query = query.filter(Invoice.invoice_status == params['invoice_status'])
                
        except Exception as ex:
            print(f"Lỗi khi lấy danh sách invoice: {ex}")
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
    
