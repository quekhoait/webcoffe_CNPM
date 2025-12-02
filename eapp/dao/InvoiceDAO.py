from eapp.models import Invoice
from eapp import db



class InvoiceDAO:
    @staticmethod
    def list(params: dict = None):
        try:
            query = Invoice.query
            if params:
                if params['is_counter']: #tại quầy
                    query = query.filter(Invoice.customer_id == None)
                else: # online
                    query = query.filter(Invoice.staff_id == None)
                
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
    def create(invoice: Invoice) -> Invoice:
        try:
            db.session.add(invoice)
            db.session.commit()
            return invoice
        except Exception as ex:
            print(f"Lỗi khi tạo invoice: {ex}")
            return None
        
    
