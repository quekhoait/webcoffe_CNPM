from eapp.models import Warehouse

class WarehouseDAO:
    @staticmethod
    def get_by_id(warehouse_id: int) -> Warehouse:
        return Warehouse.query.get(warehouse_id)
    
    @staticmethod
    def list(params: dict = None):
        try:
            query = Warehouse.query

            return query.all()
        except Exception as ex:
            print(f"Lỗi khi lấy danh sách warehouse: {ex}")
            return []
    
    
    