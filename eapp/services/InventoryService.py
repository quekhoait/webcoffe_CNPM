from enum import Enum

from eapp.dao import RuleDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.dao.WarehouseSlipDAO import WarehouseSlipDAO
from eapp.models import Ingredient, Stock, Warehouse, WarehouseSlip
from eapp.models.Invoice import Invoice
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
        return
        ingredient_id
        required_quantity
        available_quantity

        ingredients 
            ingredient_id
            quantity
    """
    @staticmethod
    def get_insufficient_ingredients(ingredients: list, warehouse_id: int):
        warehouse = WarehouseDAO.get_by_id(warehouse_id=warehouse_id)
        stocks = warehouse.stocks
        insufficient_ingredients = []
        for ingredient in ingredients:
            stock = next((s for s in stocks if s.ingredient_id == ingredient['ingredient_id']), None)
            if stock is not None:
                print(stock.ingredient_id, stock.quantity)
            if stock is None or stock.quantity < ingredient['quantity']:
                insufficient_ingredients.append({
                    'ingredient_id': ingredient['ingredient_id'],
                    'required_quantity': ingredient['quantity'],
                    'available_quantity': stock.quantity if stock else 0
                })
        return insufficient_ingredients


    """
        cafe: 2a , 2b : 2
        che: 3a, 3c : 1
    """

    @staticmethod
    def get_ingredient_list_from_invoice(invoice: Invoice):
        ingredients = {}
        for item in invoice.invoice_details:
            product = item.product
            for recipe_ingredient in product.ingredients:
                if recipe_ingredient.ingredient_id in ingredients:
                    ingredients[recipe_ingredient.ingredient_id]['quantity'] += item.quantity * recipe_ingredient.quantity
                else:
                    ingredients[recipe_ingredient.ingredient_id] = {
                        'ingredient_id' : recipe_ingredient.ingredient_id,
                        'quantity' : item.quantity * recipe_ingredient.quantity
                    }

        return ingredients

    @staticmethod
    def invoice_process(invoice: Invoice, source_warehouse_id: int):
        ingredients = list(InventoryService.get_ingredient_list_from_invoice(invoice=invoice).values())
        insufficient_ingredients = InventoryService.get_insufficient_ingredients(
            ingredients=ingredients,
            warehouse_id=source_warehouse_id
        )
        if insufficient_ingredients:
            return {
                'success' : False,
                'insufficient_ingredients' : insufficient_ingredients
            }
        slip_data = {
            'slip_type' : 'EXPORT',
            'note' : f'Xuất kho tự động cho hóa đơn #{invoice.id}',
            'stock_user_id' : None,
            'invoice_id' : invoice.id,
            'destination_warehouse_id' : None,
            'source_warehouse_id' : source_warehouse_id,
            'ingredients' : ingredients
        }
        return {
            'success' : True,
            'warehouse_slip' : InventoryService.create_slip(slip_data=slip_data)
        }



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
        return warehouse_slip

    

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

        

        