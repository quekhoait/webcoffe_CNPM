from eapp.models import InvoiceStatus


class InvoiceStatusDAO:
    def list(params: dict = None):
        try:
            query = InvoiceStatus.query
            return query.all()
        except Exception as ex:
            return []