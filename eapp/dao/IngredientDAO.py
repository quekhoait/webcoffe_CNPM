from eapp import app
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
            app.logger.error(f"Lỗi khi lấy danh sách nguyên liệu: {ex}",exc_info=True)
            return []
        return query.all()
    
    @staticmethod
    def get_by_id(ingredient_id):
        try:
            return Ingredient.query.get(ingredient_id)
        except Exception as ex:
            app.logger.error(f"Lỗi khi lấy nguyên liệu ID {ingredient_id}: {ex}",exc_info=True)
            return None