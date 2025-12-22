from pprint import pprint
from eapp import app,db
from eapp.dao import ProductDao
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Account import Account
from eapp.models.Invoice import Invoice, PaymentMethod
from eapp.models.Payment import PaymentStatus
from eapp.models.Product import Product
from eapp.services.inventory.RecipeService import RecipeService
from sqlalchemy.dialects import mysql

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

    res = RecipeService.get_stock_shortage_by_products(
        product_details=details,
        warehouse_id=1
    )

def parse_dict(objects):
    return [ o.to_dict() for o in objects ]

def test_query():

    query = Invoice.query.join(Account, Invoice.customer_id == Account.id)\
                 .filter(Account.name.like("%huy%"))\
                 .with_entities(Invoice.order_code, Account.name)
    print(query.statement)
    print(query.all())

if __name__ == '__main__':
    with app.app_context():
        # test_start_processing_invoice()
        test_query()
        # print(ProductDao.get_product_recipe_map())
        # print(WarehouseDAO.get_stock_map(1))
        # print(InventoryService.get_product_makeable_map(ProductDao.list(),1))
        # print(InventoryService.get_quantity_product_makeable(1,200,1))
        # print(InventoryService.load_stock(1))
        # print(WarehouseDAO.get_available_stock_map(1))