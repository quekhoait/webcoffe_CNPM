from eapp import app,db
from eapp.dao import ProductDao
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Product import Product
from eapp.services.InventoryService import InventoryService

if __name__ == '__main__':
    with app.app_context():
        print(ProductDao.get_product_recipe_map())
        print(WarehouseDAO.get_stock_map(1))
        print(InventoryService.get_product_makeable_map(ProductDao.list(),1))
        print(InventoryService.get_quantity_product_makeable(1,200,1))