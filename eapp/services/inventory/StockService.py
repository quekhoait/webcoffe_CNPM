from enum import Enum
from eapp.dao import RuleDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.dao.WarehouseSlipDAO import WarehouseSlipDAO
from eapp.models.Invoice import Invoice, InvoiceStatusEnum
from eapp.models.Rule import RuleType
from eapp.models.Stock import Stock
from eapp.models.WarehouseSlip import SlipType, WarehouseSlip
from eapp.services.SlipStrategyFactory import SlipStrategyFactory
from eapp.services.inventory.RecipeService import RecipeService


class IngredientStatus(Enum):
    AVAILABLE = "Còn Hàng"
    LOW_STOCK = "Sắp Hết"
    OUT_OF_STOCK = "Hết Hàng"

class StockService:

    @staticmethod
    def load_rules():
        return RuleDAO.list(RuleDAO.RuleFilter(rule_type = RuleType.INGREDIENT))

    @staticmethod
    def load_stock(warehouse_id: int):
        warehouse = WarehouseDAO.get_by_id(warehouse_id)
        stock_data = []
        for ingredient_stock in warehouse.stocks:
            status = StockService.get_ingredient_stock_status(ingredient_stock)
            stock_data.append({
                'ingredient': ingredient_stock.ingredient,
                'quantity': ingredient_stock.quantity,
                'reserved' : ingredient_stock.reserved,
                'status': status
            })
        return stock_data
    
    @staticmethod
    def get_ingredient_stock_status(ingredient_stock: Stock):
        availabble_stock = ingredient_stock.quantity - ingredient_stock.reserved
        if availabble_stock == 0:
            return IngredientStatus.OUT_OF_STOCK
        if availabble_stock < StockService.load_rules()[0].value:
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
        warehouse_slip.slip_type = SlipType[slip_data['slip_type']]
        warehouse_slip.note = slip_data['note'] if slip_data['note'] else None

        WarehouseSlipDAO.create_warehouse_slip(warehouse_slip, slip_data['ingredients'])
        # import pdb
        # pdb.set_trace()
        SlipStrategyFactory.get_strategy(warehouse_slip.slip_type).update_stock(warehouse_slip=warehouse_slip)
        return warehouse_slip
    
        """
        5000
        4900
    """
    # cộng dồn reserved cho kho
    @staticmethod
    def reserve_stock_for_invoice(invoice: Invoice,warehouse_id, used_stock = None):
        warehouse = WarehouseDAO.get_by_id(warehouse_id)
        if invoice.invoice_status == InvoiceStatusEnum.PENDING:
            if used_stock is not None:
                for stock in warehouse.stocks:
                    stock.reserved += used_stock[stock.ingredient_id]
            else:
                used_stock = RecipeService.get_ingredient_list_from_invoice(invoice)
                for stock in warehouse.stocks:
                    stock.reserved += used_stock.get(stock.ingredient_id,{}).get('quantity',0)

    """
        params:
        used_stock
        {
            ingredient_id: used_quantity
        }
        warehouse_id

    """
    #Cập nhật tồn kho của in progress
    @staticmethod
    def release_reserved_stock(used_stock, warehouse_id):
        warehouse =  WarehouseDAO.get_by_id(warehouse_id)
        for stock in warehouse.stocks:
            print(f"{stock.quantity} : {stock.reserved}")
            used_quantity = used_stock.get(stock.ingredient_id,0)
            # stock.quantity -= used_quantity
            stock.reserved -= used_quantity
