from pprint import pprint
from flask import jsonify, render_template, request
from eapp import app, db
from eapp.dao.IngredientDAO import IngredientDAO, IngredientFilter
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Ingredient import Ingredient
from eapp.models.WarehouseSlip import SlipType
from eapp.services.RuleService import RuleService
from eapp.services.inventory.InventoryValidator import InventoryValidator
from eapp.services.inventory.StockService import IngredientStatus, StockService

def get_warehouse(load_admin_stock = None):
    warehouse_id = int(request.args.get('warehouse_id',1))
    warehouse = WarehouseDAO.get_by_id(warehouse_id)
    warehouses = WarehouseDAO.list()
    slip_types = [(st.name, st.value) for st in SlipType]
    ingredient_stocks = load_admin_stock(warehouse_id) if load_admin_stock else StockService.load_stock(warehouse_id=warehouse_id)
    ingredients = IngredientDAO.list()
    low_stock_list = [
        item for item in ingredient_stocks
        if item["status"] in [IngredientStatus.LOW_STOCK, IngredientStatus.OUT_OF_STOCK]
    ]
    return {
        "warehouse": warehouse,
        "warehouses": warehouses,
        "slip_types": slip_types,
        "ingredient_stocks": ingredient_stocks,
        "ingredients": ingredients,
        "low_stock_list": low_stock_list
    }

def warehouse_page():
    data=get_warehouse()
    return render_template('warehouse/warehouse.html',
                           **data)

def warehouse_admin():
    data=get_warehouse(StockService.load_stock_for_admin)
    return render_template('admin/warehouse.html',
                           **data)

def render_warehouse_admin_ingredient_item():
    ingredient_stocks = StockService.load_stock_for_admin(
                                warehouse_id=get_current_warehouse_id(),
                                params=IngredientFilter(keyword=request.args.get('keyword'))
                            )
    pprint(ingredient_stocks)
    return render_template('admin/warehouse_ingredient_item.html',
                            ingredient_stocks = ingredient_stocks)

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
        rs = InventoryValidator.validate_slip_data(slip_data)
        if rs:
            StockService.create_slip(slip_data)
        db.session.commit()
        return jsonify({"success": True})

    except Exception as ex:
        db.session.rollback()
        app.logger.error(f"Lỗi khi tạo phiếu kho: {str(ex)}", exc_info=True)
        return jsonify({
            "success": False, 
            "message": str(ex) if str(ex) else "Đã xảy ra lỗi hệ thống khi tạo phiếu kho"
        })

def load_warehouse():
    return render_template('admin/warehouse.html',
                          )

def get_current_warehouse_id():
    return RuleService.get_rule_warehouse_id()
    