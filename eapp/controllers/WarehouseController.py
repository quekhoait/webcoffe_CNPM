from flask import jsonify, render_template, request

from eapp.dao.IngredientDAO import IngredientDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Ingredient import Ingredient
from eapp.models.WarehouseSlip import SlipType
from eapp.services.InventoryService import InventoryService


def warehouse_page():
    warehouse_id = int(request.args.get('warehouse_id', 1))
    warehouse = WarehouseDAO.get_by_id(warehouse_id)
    warehouses = WarehouseDAO.list()
    slip_types = [(st.name, st.value) for st in SlipType]
    ingredient_stocks = InventoryService.load_stock(warehouse_id=warehouse_id)
    ingredients = IngredientDAO.list()
    return render_template('warehouse/warehouse.html',
                           warehouse=warehouse,
                            slip_types=slip_types,
                           ingredient_stocks=ingredient_stocks,
                           ingredients=ingredients,
                           warehouses=warehouses)

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
    print(slip_data)
    try:
        InventoryService.create_slip(slip_data)
    except Exception as ex:
        print(f"Lỗi khi tạo phiếu kho: {ex}")
        return jsonify({"success": False, "message": str(ex)})
    return jsonify({"success": True})