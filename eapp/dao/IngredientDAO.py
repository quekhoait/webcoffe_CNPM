from eapp.models import Ingredient


class IngredientDAO:
    @staticmethod
    def list(params: dict = None):
        try:
            query = Ingredient.query
        except Exception as ex:
            print(f"Lỗi khi lấy danh sách nguyên liệu: {ex}")
            return []
        return query.all()