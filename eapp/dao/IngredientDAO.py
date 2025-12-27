from eapp import app, db
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

def add_ingredient(data):
    try:
        new_ingre = Ingredient(
            name=data.get('name'),
            price=data.get('price'),
            unit=data.get('unit'),
            description=data.get('description'),
        )
        db.session.add(new_ingre)
        db.session.commit()
        return True
    except Exception as ex:
        print(f"Lỗi thêm: {ex}")
        db.session.rollback()
        return False

# def update_product(product_id, data, recipes=None):
#     try:
#         product = Product.query.get(product_id)
#         if not product: return False
#
#         product.name = data.get('name')
#         product.price = data.get('price')
#         product.unit = data.get('unit')
#         product.dish_category_id = data.get('dish_category_id')
#         product.description = data.get('description')
#         if data.get('image'):
#             product.image = data.get('image')
#
#         #cập nhật công thức nếu có
#         if recipes is not None:
#             #xóa công thức cũ -> thêm công thức mới
#             ProductRecipe.query.filter_by(product_id=product_id).delete()
#             for item in recipes:
#                 if item.get('ingredient_id'):
#                     new_recipe = ProductRecipe(
#                         product_id=product.id,
#                         ingredient_id=item['ingredient_id'],
#                         quantity=item['quantity'],
#                         unit=item['unit']
#                     )
#                     db.session.add(new_recipe)
#
#         db.session.commit()
#         return True
#     except Exception as ex:
#         print(f"Lỗi sửa: {ex}")
#         db.session.rollback()
#         return False
#
# def delete_product(product_id):
#     try:
#         product = Product.query.get(product_id)
#         if product:
#             ProductRecipe.query.filter_by(product_id=product_id).delete()
#             db.session.delete(product)
#             db.session.commit()
#             return True
#         return False
#     except Exception as ex:
#         db.session.rollback()
#         return False
