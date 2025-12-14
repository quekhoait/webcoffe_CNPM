from eapp import app
from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.services.InventoryService import InventoryService

if __name__ == '__main__':
    with app.app_context():  
        invoice = InvoiceDAO.get_by_id(1)
        print(invoice)
        list_ingredients = InventoryService.get_ingredient_list_from_invoice(invoice)
        rs = InventoryService.get_insufficient_ingredients(
            ingredients=list(list_ingredients.values()),
            warehouse_id=1
        )
        print(rs)
