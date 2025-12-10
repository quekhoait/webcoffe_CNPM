from flask import render_template

from eapp.dao.IngredientDAO import IngredientDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Ingredient import Ingredient
from eapp.models.WarehouseSlip import SlipType
from eapp.services.InventoryService import InventoryService


def warehouse_page():

    warehouse = WarehouseDAO.get_by_id(1)
    warehouses = WarehouseDAO.list()
    slip_types = [(st.name, st.value) for st in SlipType]
    ingredient_stocks = InventoryService.load_stock(warehouse_id=1)
    ingredients = IngredientDAO.list()
    return render_template('warehouse/warehouse.html',
                           warehouse=warehouse,
                            slip_types=slip_types,
                           ingredient_stocks=ingredient_stocks,
                           ingredients=ingredients,
                           warehouses=warehouses)