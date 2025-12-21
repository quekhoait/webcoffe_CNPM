from eapp.dao import ProductDao
from eapp.models.Invoice import Invoice


class RecipeService:
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
    # tính tổng nguyên liệu yêu cầu từ danh sách product
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
    # thấy map theo tổng nguyên liệu
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
    #lấy map của danh sách nguyên liệu yêu cầu theo product
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
    # Lấy từ điển nguyên liệu theo yêu cầu product
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
