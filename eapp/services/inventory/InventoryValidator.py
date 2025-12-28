import pdb
from pprint import pprint
from eapp.dao import ProductDao
from eapp.dao.IngredientDAO import IngredientDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.services.inventory.RecipeService import RecipeService
from eapp.services.inventory.StockService import StockService


class InventoryValidator:
    
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
        required_ingredient_map = RecipeService.aggregate_ingredient_demand_by_product(product_details,product_recipe_map)

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
    

    """
        quantity_product: khả năng đáp ứng dựa trên số lượng
    """
    # Kiểm tra theo product này đủ không
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

        available_stock_map
        {
            ingredient_id : quantity
        }

    """
    # kiểm tra xem product này đủ không, ko thì trả về lý do ko đủ
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
        [
            Product,
            Product
        ]

        {
            product_id:bool,
            product_id:bool,
        }
    """
    # Đánh các nguyên liệu đủ phục vụ hoặc ko hoặc ko công thức
    def get_product_makeable_map(products, warehouse_id):
        available_stock_map = WarehouseDAO.get_available_stock_map(warehouse_id)
        recipe_map = ProductDao.get_product_recipe_map()
        result = {}
        for product in products:
            result[product.id] = not InventoryValidator.is_product_insufficient(product.id,recipe_map,available_stock_map)
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
    # xem xét bỏ hàm
    def get_insufficient_products(invoice_items: list, warehouse_id):
        available_stock_map = WarehouseDAO.get_available_stock_map(warehouse_id)
        required_ingredient_map = RecipeService.calculate_required_ingredients(invoice_items)
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
    slip_data:
        slip_type
        note
        stock_user_id
        invoice_id (option)
        destination_warehouse_id
        source_warehouse_id
        ingredients (list)
            ingredient_id
            quantity
    """
    def validate_slip_data(slip_data):
        slip_type = slip_data.get('slip_type')
        ingredients = slip_data.get('ingredients', [])
        src_id = slip_data.get('source_warehouse_id')
        dest_id = slip_data.get('destination_warehouse_id')

        if not ingredients:
            raise Exception("Danh sách nguyên liệu không được để trống")

        if slip_type == 'IMPORT':
            if not dest_id: raise Exception("Phải chỉ định kho để nhập hàng")
        
        elif slip_type in ['EXPORT', 'UPDATE']:
            if not src_id: raise Exception("Phải chọn kho nguồn")
            
        elif slip_type == 'TRANSFER':
            if not src_id or not dest_id:
                raise Exception("Chuyển kho cần có cả kho nguồn và kho đích")
            if src_id == dest_id:
                raise Exception("Kho nguồn và kho đích không được trùng nhau")
        current_stock = {}
        if src_id:
            current_stock = WarehouseDAO.get_stock_map(src_id)
        for item in ingredients:
            ing_id = int(item.get('ingredient_id')) 
            quantity = float(item.get('quantity'))

            if not ing_id: raise Exception("Dữ liệu nguyên liệu không hợp lệ")
            if quantity <= 0: raise Exception("Số lượng phải lớn hơn 0")

            if slip_type in ['EXPORT', 'TRANSFER']:
                if quantity > current_stock.get(ing_id,None).get('available',0):
                    ing_name = IngredientDAO.get_by_id(ing_id).name
                    raise Exception(f"Nguyên liệu {ing_name} không đủ tồn kho (Hiện có: {current_stock.get(ing_id,0)})")
            elif slip_type in ['UPDATE']:
                if quantity < current_stock.get(ing_id,None).get('reserved',0):
                    ing_name = IngredientDAO.get_by_id(ing_id).name
                    raise Exception(f"Nguyên liệu {ing_name} không đủ tồn kho (Hiện có: {current_stock.get(ing_id,0)})")
        return True