from dataclasses import dataclass
from typing import Optional

from sqlalchemy import and_
from eapp import app,db
from eapp.models import Ingredient, Stock


@dataclass
class IngredientFilter:
    keyword : Optional[str] = None

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
    def list_stock_by_warehouse_id(params : IngredientFilter = None, warehouse_id=None):

        try:
            query = db.session.query(Ingredient,Stock).outerjoin(
                Stock,
                and_(
                    Stock.ingredient_id == Ingredient.id,
                    Stock.warehouse_id == warehouse_id
                )
            )

            if params:
                if params.keyword:
                    query = query.filter(Ingredient.name.ilike(f"%{params.keyword}%"))
            
            return query.all()
        except Exception as ex:
            app.logger.error(f"Lỗi khi lấy nguyên liệu với stock: {ex}", exc_info=True)
            return []

    @staticmethod
    def get_by_id(ingredient_id):
        try:
            return Ingredient.query.get(ingredient_id)
        except Exception as ex:
            app.logger.error(f"Lỗi khi lấy nguyên liệu ID {ingredient_id}: {ex}",exc_info=True)
            return None
        