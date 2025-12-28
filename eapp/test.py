from pprint import pp, pprint

from eapp import app,db
from eapp.dao import ProductDao
from eapp.dao.IngredientDAO import IngredientFilter
from eapp.dao.InvoiceDAO import InvoiceDAO, InvoiceFilter
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models.Account import Account
from eapp.models.Invoice import Invoice, InvoiceStatusEnum, PaymentMethod
from eapp.models.Payment import PaymentStatus
from eapp.models.Product import Product
from eapp.services.RuleService import RuleService
from eapp.services.inventory.StockService import StockService
from eapp.services.inventory.InventoryValidator import InventoryValidator
from eapp.services.inventory.RecipeService import RecipeService
from sqlalchemy.dialects import mysql

"""
<!-- Đang chọn -->
<div data-status="selecting" class="active-invoice-card invoice-card p-4 rounded-xl shadow-md ">
    <!-- Mã đơn + trạng thái -->
    <div class="flex justify-between items-center">
        <span class="text-2xl font-extrabold tracking-wide text-amber-900">
            #000001
        </span>

        <span class="text-lg font-semibold text-amber-900 px-3 py-1 bg-amber-200/70 rounded-full shadow">
            Chờ xử lý
        </span>
    </div>

    <!-- Khách + thời gian -->
    <div class="flex justify-between items-center text-gray-700">
        <span class="text-lg font-medium">
            Ho Mai Huong
        </span>

        <span class="text-lg px-2 py-0.5 rounded-md bg-white text-amber-700 font-semibold tracking-wide">
            10:32
        </span>
    </div>

    <!-- Tổng + phương thức -->
    <div class="flex justify-between items-end pt-1">
        <span class="text-2xl text-amber-900 font-extrabold leading-none">
            999.999 USD
        </span>

        <span  data-method="cash" class="payment-method">
            Tiền mặt
        </span>
    </div>
</div>

"""

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

def demo():
    data = [
        {
            'product_id' : 1,
            'quantity' : 150
        },
        {
            'product_id' : 2,
            'quantity' : 50
        }
    ]
    kq = InventoryValidator.get_insufficient_products(data,1)
    print(kq)
    print(WarehouseDAO.get_available_stock_map(1))
    pprint(ProductDao.get_product_recipe_map())


if __name__ == '__main__':
    with app.app_context():
        # test_start_processing_invoice()
        rs = StockService.load_stock_for_admin(1,IngredientFilter(keyword = "s"))
        pprint(rs)
        # print(RuleService.get_rule_warehouse_id())
        # print(ProductDao.get_product_recipe_map())
        # print(WarehouseDAO.get_stock_map(1))
        # print(InventoryService.get_product_makeable_map(ProductDao.list(),1))
        # print(InventoryService.get_quantity_product_makeable(1,200,1))
        # print(InventoryService.load_stock(1))
        # print(WarehouseDAO.get_available_stock_map(1))
        