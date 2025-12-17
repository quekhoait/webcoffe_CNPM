# from eapp.models import InvoiceDetail
# from eapp import db

# class InvoiceDetailDAO:
#     @staticmethod

#     def create(data: dict) -> InvoiceDetail:
#         try:
#             invoice_detail = InvoiceDetail(**data)
#             db.session.add(invoice_detail)
#             db.session.commit()
#             return invoice_detail
#         except Exception as ex:
#             db.session.rollback()
#             print(f"Lỗi khi tạo invoice detail: {ex}")
#             return None
        
#     @staticmethod
#     def create(invoice_details: list) -> list:
#         created_details = []
#         try:
#             for detail in invoice_details:
#                 db.session.add(detail)
#                 created_details.append(detail)
#             db.session.commit()
#             return created_details
#         except Exception as ex:
#             db.session.rollback()
#             print(f"Lỗi khi tạo invoice details: {ex}")
#             return []