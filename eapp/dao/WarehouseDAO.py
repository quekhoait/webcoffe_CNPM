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
    
    @staticmethod
    def update(stock: Warehouse):
        try:
            stock.save()
            return stock
        except Exception as ex:
            print(f"Lỗi khi cập nhật warehouse: {ex}")
            return None

    @staticmethod    
    def get_available_stock_map(warehouse_id):
     
        warehouse = WarehouseDAO.get_by_id(warehouse_id=warehouse_id)
        return {
            stock.ingredient_id : stock.quantity - stock.reserved
            for stock in warehouse.stocks
        }
    
    
    