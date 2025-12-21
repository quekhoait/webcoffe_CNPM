from enum import Enum
from unittest import result

from eapp.dao import ProductDao, RuleDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.dao.WarehouseSlipDAO import WarehouseSlipDAO
from eapp.models import Ingredient, Stock, Warehouse, WarehouseSlip
from eapp.models.Invoice import Invoice, InvoiceStatusEnum
from eapp.models.Product import Product
from eapp.models.Rule import RuleType
from eapp.services.SlipStrategyFactory import SlipStrategyFactory

class IngredientStatus(Enum):
    AVAILABLE = "Còn Hàng"
    LOW_STOCK = "Sắp Hết"
    OUT_OF_STOCK = "Hết Hàng"

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
                'reserved' : ingredient_stock.reserved,
                'status': status
            })
        return stock_data
        
    @staticmethod
    def load_rules():
        return RuleDAO.list({'rule_type': RuleType.INGREDIENT})

    @staticmethod
    def get_ingredient_stock_status(ingredient_stock: Stock):
        availabble_stock = ingredient_stock.quantity - ingredient_stock.reserved
        if availabble_stock == 0:
            return IngredientStatus.OUT_OF_STOCK
        if availabble_stock < InventoryService.load_rules()[0].value:
            return IngredientStatus.LOW_STOCK
        return IngredientStatus.AVAILABLE
    


    """
    params
        invoice_details:
        [
            {
                product_id,
                quantity
            }
        ]
        warehouse_id
    return
        {
            insufficient_ingredients 
            [
                {
                    ingredient_id,
                    required_quantity,
                    available_quantity
                }
            ]

            effected_products
            [
                product_id
            ]
        }
    """
    @staticmethod
    def get_stock_shortage_by_products(product_details, warehouse_id, available_stock_map=None, product_recipe_map=None):
        # import pdb
        # pdb.set_trace()
        if available_stock_map is None:
            available_stock_map = WarehouseDAO.get_available_stock_map(warehouse_id)
        if product_recipe_map is None:
            product_recipe_map = ProductDao.get_product_recipe_map()
        insufficient_ingredients = []
        shortage_ingredient_id = set()
        effected_products = []
        required_ingredient_map = InventoryService.aggregate_ingredient_demand_by_product(product_details,product_recipe_map)

        for ingredient_id, required_quantity in required_ingredient_map.items():
            available = available_stock_map.get(ingredient_id,0)
            #thiếu thì bỏ qua, đánh dấu
            if available < required_quantity:
                shortage_ingredient_id.add(ingredient_id)
                insufficient_ingredients.append(
                    {
                        'ingredient_id' : ingredient_id,
                        'required_quantity' : required_quantity,
                        'available_quantity' : available
                    }
                ) 
            else:
                #đủ thì trừ đi cho món ở phía trước, món sau ko sài lại
                available_stock_map[ingredient_id] -= required_quantity
        
        # tìm product bị ảnh hưởng
        for product in product_details:
            product_id = product['product_id']
            if any(ing['ingredient_id'] in shortage_ingredient_id for ing in product_recipe_map[product_id] ):
                effected_products.append(product_id)

                
        return {
            'insufficient_ingredients': insufficient_ingredients,
            'effected_products': effected_products
        }

        # for ingredient in ingredients:
        #     stock = next((s for s in stocks if s.ingredient_id == ingredient['ingredient_id']), None)
        #     # if stock is not None:
        #         # print(stock.ingredient_id, stock.quantity)
        #     if stock is None or stock.quantity < ingredient['quantity']:
        #         insufficient_ingredients.append({
        #             'ingredient_id': ingredient['ingredient_id'],
        #             'required_quantity': ingredient['quantity'],
        #             'available_quantity': stock.quantity if stock else 0
        #         })
        # return insufficient_ingredients
    

    """
    params
        product_details:
        [
            {
                product_id,
                quantity
            }
        ]

        product_recipe_map
        {
            product_id
            [
                {
                    ingredient_id,
                    quantity    
                }
            ]
        }

    return
        total_ingredient_demand
        {
            ingredient_id : required_quantity
        }
    """
    @staticmethod
    def aggregate_ingredient_demand_by_product(product_details: list, product_recipe_map: dict):
        total_ingredient_demand = {}
        for product in product_details:
            product_id = product['product_id']
            # lấy nguyên liệu từng sản phẩm 
            for ingredient in product_recipe_map[product_id]:
                # tính tổng nguyên liệu sản phẩm cần
                required_quantity = ingredient['quantity'] * product['quantity']
                ingredient_id = ingredient['ingredient_id']
                # cộng dồn ingredient giống nhau
                if ingredient_id in total_ingredient_demand:
                    total_ingredient_demand[ingredient_id] += required_quantity
                else:
                    total_ingredient_demand[ingredient_id] = required_quantity
        return total_ingredient_demand

    """
    return
        {
            ingredient_id : 
            {
                ingredient_id,
                quantity
            }
        }
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
    
    """
        quantity_product: khả năng đáp ứng dựa trên số lượng
    """
    
    @staticmethod
    def is_product_insufficient(product_id, recipe_map, available_stock_map , quantity_product = 1):
        recipe = recipe_map.get(product_id, [])
        if not recipe:
            return True
        
        for ingredient in recipe:
            available = available_stock_map.get(ingredient['ingredient_id'],0)
            required = ingredient['quantity'] * quantity_product
            if available < required:
                return True
        return False

    """
        {
            product_id,
            quantity,
            ingredient_insufficient [{
                ingredient_id,
                available,
                required
            }]
            makeable_quantity
        }
    """
    @staticmethod
    def get_quantity_product_makeable(product_id,quantity,available_stock_map):

        recipe_map = ProductDao.get_product_recipe_map()
        recipe = recipe_map.get(product_id, [])

        if not recipe:
            return {
                "product_id": product_id,
                "quantity": quantity,
                "ingredient_insufficient": [],
                "makeable_quantity": 0
            }

        max_quantities = []
        ingredient_insufficient = []
        result = {}
        for ing in recipe:
            ingredient_id = ing['ingredient_id']
            ing_per_product = ing['quantity']

            available = available_stock_map.get(ingredient_id,0)

            if ing_per_product <= 0:
                continue

            max_quantity_product_per_ingredient = int(available // ing_per_product)
            max_quantities.append(max_quantity_product_per_ingredient)

            required = ing_per_product * quantity
            if available < required:
                ingredient_insufficient.append(
                    {
                        'ingredient_id' : ingredient_id,
                        'available' : available,
                        'required' : required
                    }
                )
        
        makeable_quantity = min(max_quantities)
        return {
            'product_id' : product_id,
            'quantity' : quantity,
            'ingredient_insufficient' : ingredient_insufficient,
            'makeable_quantity' : makeable_quantity
        }



    """
        {
            product_id:bool,
            product_id:bool,
        }
    """
    def get_product_makeable_map(products, warehouse_id):
        available_stock_map = WarehouseDAO.get_available_stock_map(warehouse_id)
        recipe_map = ProductDao.get_product_recipe_map()
        result = {}
        for product in products:
            result[product.id] = not InventoryService.is_product_insufficient(product.id,recipe_map,available_stock_map)
        return result        
    
        
    

    # tạo phiếu xuất kho cho hóa đơn
    @staticmethod
    def start_processing_invoice(invoice: Invoice, source_warehouse_id: int):

        #check tồn kho lần nữa
        result = InventoryService.get_stock_shortage_by_products(
            product_details=invoice.invoice_details,
            available_stock_map=WarehouseDAO.get_available_stock_map(source_warehouse_id),
            product_recipe_map= ProductDao.get_product_recipe_map()
        )
        if result['insufficient_ingredients']:
            return {
                'success' : False,
                'data' : {
                    'insufficient_ingredients' : result['insufficient_ingredients'],
                    'effected_products' : result['effected_products']
                }
            }
        
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

        # hoàn lại reserved
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

    """
    params
        [
            {
                product_id,
                name,
                price,
                quantity
            }
        ]

    return
        {
            product_id : [
                {
                    ingredient_id,
                    required_quanity
                }
            ]
        }

    recipe_map
        {
            product_id (int) : 
            [
                {
                    ingredient_id,
                    quantity
                }
            ]
        }
    """
    @staticmethod
    def calculate_required_ingredients(invoice_items):
        recipe_map = ProductDao.get_product_recipe_map()
        result = {}
        for product in invoice_items:
            product_id = int(product['product_id'])
            required_list = []
            for ing in recipe_map[product_id]:
                required_list.append(
                    {
                        'ingredient_id' : ing['ingredient_id'],
                        'required_quanity' : ing['quantity'] * product['quantity']
                    }
                )
            result[product_id] = required_list

        return result


    """
        params
        [
            {
                product_id,
                name, * ko cần
                price, * ko cần
                quantity
            }
        ]
    
       return
        [
            {
                product_id,
                required_quantity,
                makeable_quantity
            }
        ]
    
    """
    def get_insufficient_products(invoice_items: list, warehouse_id):

        available_stock_map = WarehouseDAO.get_available_stock_map(warehouse_id)
        required_ingredient_map = InventoryService.calculate_required_ingredients(invoice_items)
        recipe_map = ProductDao.get_product_recipe_map()

        result = []
        # lặp qua từng product
        for product in invoice_items:
            max_quantities = []
            is_insufficient = False
            product_id = int(product['product_id'])
            # lấy quantity nguyên liệu của product yêu cầu, và nguyên liệu của công thức product ing_required: 1:20 ing_recipe 1:10
            for ing_required, ing_recipe in zip(required_ingredient_map[product_id],recipe_map[product_id]):
                required = ing_required['required_quanity']
                available = available_stock_map[ing_required['ingredient_id']]
                ing_per_product = ing_recipe['quantity']
                max_quantities.append(int(available // ing_per_product))

                # không break, ưu tiên nguyên liệu cho các món trên, đã sài thì trừ ra, món dưới thiếu thì báo 
                if available < required:
                    is_insufficient = True
                    continue

  
                available_stock_map[ing_required['ingredient_id']] = available_stock_map[ing_required['ingredient_id']] - required
            if is_insufficient:
                result.append(
                    {
                        'product_id':product_id,
                        'required_quantity': product['quantity'],
                        'makeable_quantity' : min(max_quantities)
                    }
                )


        return result , available_stock_map

    """     
    params
    [
        {
            product_id,
            name,
            price,
            quantity
        }
    ]

    return
    {
        ingredient_id : quantity
    }
    """
    @staticmethod
    def get_required_ingredient_map_from_session_invoice(invoice_items):
        recipe_map = ProductDao.get_product_recipe_map()
        result = {}
        for product in invoice_items:
            product_id = int(product['product_id'])
            for ing in recipe_map[product_id]:
                if ing['ingredient_id'] in result:
                    result[ing['ingredient_id']] += ing['quantity'] * product['quantity']
                else:
                    result[ing['ingredient_id']] = ing['quantity'] * product['quantity']
        return result

    """
        5000
        4900
    """
    @staticmethod
    def reserve_stock_for_invoice(invoice: Invoice,warehouse_id, used_stock = None):
        warehouse = WarehouseDAO.get_by_id(warehouse_id)
        if invoice.invoice_status == InvoiceStatusEnum.PENDING:
            if used_stock is not None:
                for stock in warehouse.stocks:
                    stock.reserved += used_stock[stock.ingredient_id]
            else:
                used_stock = InventoryService.get_ingredient_list_from_invoice(invoice)
                for stock in warehouse.stocks:
                    stock.reserved += used_stock.get(stock.ingredient_id,{}).get('quantity',0)
        

        
    

    

from eapp import app
if __name__ == "__main__":
    with app.app_context():
        warehouse = WarehouseDAO.get_by_id(1)
        print(warehouse.stocks)    

        

        