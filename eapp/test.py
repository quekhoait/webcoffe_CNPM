from pprint import pprint

from eapp import app,db
from eapp.dao import ProductDao, CartDao
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Product import Product
from eapp.services.inventory import InventoryValidator

from eapp.services.inventory.InventoryValidator import InventoryValidator


# def test_start_processing_invoice():
#     details = [
#         {
#             'product_id' : 1,
#             'quantity' : 2
#         },
#
#         {
#             'product_id' : 2,
#             'quantity' : 2
#         }
#     ]
#
#     res = InventoryService.get_stock_shortage_by_products(
#         product_details=details,
#         warehouse_id=1
#     )
#
#     print(res)


def cart():
    cart_items = CartDao.get_cart_by_userId_dao(4)
    invoice_items = [ {'product_id' : c.product_id, 'quantity': c.quantity } for c in cart_items ]
    print(invoice_items)
    kq = InventoryValidator.get_insufficient_products(invoice_items,1)
    pprint(kq)
if __name__ == '__main__':
    with app.app_context():
        cart()
        # test_start_processing_invoice()
        # print(ProductDao.get_product_recipe_map())
        # print(WarehouseDAO.get_stock_map(1))
        # print(InventoryService.get_product_makeable_map(ProductDao.list(),1))
        # print(InventoryService.get_quantity_product_makeable(1,200,1))
        # print(InventoryService.load_stock(1))
        # print(WarehouseDAO.get_available_stock_map(1))