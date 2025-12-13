from eapp.models import Ingredient


class IngredientDAO:
    @staticmethod
    def list(params: dict = None):
        try:
            query = Ingredient.query
            if params:
                if 'name' in params:
                    query = query.filter(Ingredient.name.contains(params['name']))
                
        except Exception as ex:
            print(f"Lỗi khi lấy danh sách nguyên liệu: {ex}")
            return []
        return query.all()