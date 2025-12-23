from eapp import db
from eapp.models import Stock, Warehouse, WarehouseSlip, WarehouseSlipDetail


class SlipStrategy:
    def update_stock(self, warehouse_slip: WarehouseSlip):
        raise NotImplementedError
    
    def edit_stock(self,warehouse: Warehouse,slip_detail: WarehouseSlipDetail, updater):
        stock = next((s for s in warehouse.stocks if s.ingredient_id == slip_detail.ingredient_id), None)
        if stock:
            updater(stock,slip_detail.quantity)
        else:
            new_stock = Stock(
                    warehouse_id=warehouse.id,
                    ingredient_id=slip_detail.ingredient_id,
                    quantity=slip_detail.quantity
                )
            warehouse.stocks.append(new_stock)
        