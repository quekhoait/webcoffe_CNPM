from enum import Enum

from eapp.dao import RuleDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.dao.WarehouseSlipDAO import WarehouseSlipDAO
from eapp.models import Ingredient, Stock, Warehouse, WarehouseSlip
from eapp.models.Rule import RuleType
from eapp.services.SlipStrategyFactory import SlipStrategyFactory

class IngredientStatus(Enum):
    AVAILABLE = "Còn Hàng"
    LOW_STOCK = "Sắp Hết"

class InventoryService:
    
    @staticmethod
    def load_stock(warehouse_id: int):
        warehouse = WarehouseDAO.get_by_id(warehouse_id)
        stock_data = []
        for ingredient_stock in warehouse.stocks:
            status = InventoryService.get_ingredient_stock_status(ingredient_stock)
            stock_data.append({
                'ingredient': ingredient_stock.ingredient,
                'quantity': ingredient_stock.quantity,
                'status': status
            })
        return stock_data
        
    @staticmethod
    def load_rules():
        return RuleDAO.list({'rule_type': RuleType.INGREDIENT})

    @staticmethod
    def get_ingredient_stock_status(ingredient_stock: Ingredient):
        if ingredient_stock.quantity < InventoryService.load_rules()[0].value:
            return IngredientStatus.LOW_STOCK
        return IngredientStatus.AVAILABLE
    

    """
    slip_data:
        slip_type: name:String
        note
        stock_user_id
        invoice_id (option)
        destination_warehouse_id
        source_warehouse_id
        ingredients (list)
            ingredient_id
            quantity
    """
    @staticmethod
    def create_slip(slip_data: dict):
        warehouse_slip = WarehouseSlip()
        warehouse_slip.stock_user_id = slip_data['stock_user_id']
        src_wh_id = slip_data['source_warehouse_id']
        dst_wh_id = slip_data['destination_warehouse_id']

        # nhập kho
        if dst_wh_id is not None:
            warehouse_slip.destination_warehouse_id = dst_wh_id
        
        # xuất kho
        if src_wh_id is not None:
            warehouse_slip.source_warehouse_id = src_wh_id
        
        # parse string về enum
        warehouse_slip.slip_type = slip_data['slip_type']
        warehouse_slip.note = slip_data['note'] if slip_data['note'] else None

        WarehouseSlipDAO.create_warehouse_slip(warehouse_slip, slip_data['ingredients'])
        # import pdb
        # pdb.set_trace()
        SlipStrategyFactory.get_strategy(warehouse_slip.slip_type).update_stock(warehouse_slip=warehouse_slip)

    

    # @staticmethod
    # def update_warehouse_stock(warehouse_slip: WarehouseSlip):
    #     warehouse = WarehouseDAO.get_by_id(warehouse_id=warehouse_slip.destination_warehouse_id)
    #     for slip_detail in warehouse_slip.slip_details:
    #         stock = next((s for s in warehouse.stocks if s.ingredient_id == slip_detail.ingredient_id), None)
    #         if stock:
    #             if warehouse_slip.slip_type == 'EXPORT':
    #                 stock.quantity -= slip_detail.quantity
    #             stock.quantity += slip_detail.quantity
    #         else:
    #             new_stock = Stock(
    #                 warehouse_id=warehouse.id,
    #                 ingredient_id=slip_detail.ingredient_id,
    #                 quantity=slip_detail.quantity
    #             )
    #             warehouse.stocks.append(new_stock)
    #     warehouse.save_all(warehouse.stocks)


from eapp import app
if __name__ == "__main__":
    with app.app_context():
        warehouse = WarehouseDAO.get_by_id(1)
        print(warehouse.stocks)    

        

        