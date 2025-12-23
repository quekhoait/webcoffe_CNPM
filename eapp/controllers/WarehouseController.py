from pprint import pprint
from flask import jsonify, render_template, request
from eapp import app, db
from eapp.dao.IngredientDAO import IngredientDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Ingredient import Ingredient
from eapp.models.WarehouseSlip import SlipType
from eapp.services.inventory.StockService import IngredientStatus, StockService


def warehouse_page():
    warehouse_id = int(request.args.get('warehouse_id', 1))
    warehouse = WarehouseDAO.get_by_id(warehouse_id)
    warehouses = WarehouseDAO.list()
    slip_types = [(st.name, st.value) for st in SlipType]
    ingredient_stocks = StockService.load_stock(warehouse_id=warehouse_id)
    ingredients = IngredientDAO.list()
    low_stock_list = [
    item for item in ingredient_stocks
    if item["status"] in [IngredientStatus.LOW_STOCK,IngredientStatus.OUT_OF_STOCK]
]
    pprint(low_stock_list)
    return render_template('warehouse/warehouse.html',
                           warehouse=warehouse,
                            slip_types=slip_types,
                           ingredient_stocks=ingredient_stocks,
                           ingredients=ingredients,
                           warehouses=warehouses,
                           low_stock_list=low_stock_list)

#API
def get_ingredients():
    ingredients = IngredientDAO.list(request.args.to_dict())
    return jsonify([ i.to_dict() for i in ingredients])

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
def create_warehouse_slip():
    slip_data = request.json
    slip_data['stock_user_id'] = 1  # TODO: Lấy user từ session
    try:
        StockService.create_slip(slip_data)
        db.session.commit()
        return jsonify({"success": True})

    except Exception as ex:
        db.session.rollback()
        app.logger.error(f"Lỗi khi tạo phiếu kho: {str(ex)}", exc_info=True)
        return jsonify({"success": False, "message": "Đã xảy ra lỗi hệ thống khi tạo phiếu kho"})