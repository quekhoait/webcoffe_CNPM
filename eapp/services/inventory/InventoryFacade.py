import eapp
from eapp import app
from eapp.dao import ProductDao
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Invoice import Invoice
from eapp.services.inventory.InventoryValidator import InventoryValidator
from eapp.services.inventory.RecipeService import RecipeService
from eapp.services.inventory.StockService import StockService
from eapp import db

class InventoryFacade:
    # tạo phiếu xuất kho cho hóa đơn
    @staticmethod
    def start_processing_invoice(invoice: Invoice, source_warehouse_id: int):
        invoice_details = [ {'product_id' : detail.product_id, 'quantity' : detail.quantity}  for detail in invoice.invoice_details ]
        product_recipe_map = ProductDao.get_product_recipe_map()
        #check tồn kho lần nữa
        result = InventoryValidator.get_stock_shortage_by_products(
            product_details=invoice_details,
            available_stock_map=WarehouseDAO.get_available_stock_map(source_warehouse_id),
            product_recipe_map= product_recipe_map,
            warehouse_id=source_warehouse_id
        )
        if result['insufficient_ingredients']:
            return {
                'success' : False,
                'data' : {
                    'insufficient_ingredients' : result['insufficient_ingredients'],
                    'effected_products' : result['effected_products']
                }
            }
        

        ingredients = RecipeService.aggregate_ingredient_demand_by_product(
            product_details=invoice_details,
            product_recipe_map=product_recipe_map
        )

        # try:
        # hoàn lại reserved
        StockService.release_reserved_stock(used_stock=ingredients,
                                    warehouse_id=source_warehouse_id)

        ingredients = [
            {'ingredient_id':key , 'quantity' : value}
            for key,value in ingredients.items()
        ]
        # tạo phiếu xuất kho cho hóa đơn / trừ nguyên thật
        slip_data = {
            'slip_type' : 'EXPORT',
            'note' : f'Xuất kho tự động cho hóa đơn #{invoice.id}',
            'stock_user_id' : None,
            'invoice_id' : invoice.id,
            'destination_warehouse_id' : None,
            'source_warehouse_id' : source_warehouse_id,
            'ingredients' : ingredients
        }

        StockService.create_slip(slip_data=slip_data)
        
        return {
            'success' : True,
            'warehouse_slip' : slip_data
        }
    
    def cancel_processing_invoice(invoice: Invoice, source_warehouse_id: int):
        product_details  = [ 
            {
                'product_id' : p.product_id,
                'quantity' : p.quantity
            }
            for p in invoice.invoice_details
         ]
        used_stock = RecipeService.aggregate_ingredient_demand_by_product(
            product_details=product_details,
            product_recipe_map=ProductDao.get_product_recipe_map()
        )
        StockService.release_reserved_stock(used_stock,source_warehouse_id)

