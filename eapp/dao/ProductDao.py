from eapp.models import Product

def list(params: dict = None):
    try:
        query = Product.query

        
        if params:
            if 'dish_category_id' in params:
                query = query.filter(Product.dish_category_id == params['dish_category_id'])

            if 'name' in params:
                query = query.filter(Product.name.contains(params['name']))

        return query.all()

    except Exception as ex:
        print(f"Lỗi khi lọc món: {ex}")
        return []
    

def get_by_id(id):
    try:
        return Product.query.get(id)
    except Exception as ex:
        print(f"Lỗi khi món theo id: {ex}")
        return None



        