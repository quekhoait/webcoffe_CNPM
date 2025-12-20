from eapp import app,db
from eapp.controllers import EmployeeController
from eapp.dao import ProductDao, AccountDAO
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Product import Product
from eapp.services.InventoryService import InventoryService

def test_start_processing_invoice():
    details = [
        {
            'product_id' : 1,
            'quantity' : 2
        },

        {
            'product_id' : 2,
            'quantity' : 2
        }
    ]

    res = InventoryService.get_stock_shortage_by_products(
        product_details=details,
        warehouse_id=1
    )

    print(res)

if __name__ == '__main__':
    with app.app_context():
        # test_start_processing_invoice()
        print( [ u.to_dict() for u in AccountDAO.get_all_employees() ])
        # print(ProductDao.get_product_recipe_map())
        # print(WarehouseDAO.get_stock_map(1))
        # print(InventoryService.get_product_makeable_map(ProductDao.list(),1))
        # print(InventoryService.get_quantity_product_makeable(1,200,1))
        # print(InventoryService.load_stock(1))
        # print(WarehouseDAO.get_available_stock_map(1))