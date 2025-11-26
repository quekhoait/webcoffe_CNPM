from eapp.models import Dish
class DishDAO:
    @staticmethod
    def list(params: dict):
        try:
            query = Dish.query
            
            if 'dish_category_id' in params:
                query = query.filter(Dish.dish_category_id == params['dish_category_id'])

            if 'name' in params:
                query = query.filter(Dish.name.contains(params['name']))

            return query.all()

        except Exception as ex:
            print(f"Lỗi khi lọc món: {ex}")
            return []
        
    @staticmethod
    def get_by_id(id):
        try:
            return Dish.query.get(id)
        except Exception as ex:
            print(f"Lỗi khi món theo id: {ex}")
            return None

    

            