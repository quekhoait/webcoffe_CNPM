
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models import Stock
from eapp.services.SlipStrategy import SlipStrategy


class ExportStrategy(SlipStrategy):
    def update_stock(self, warehouse_slip):
        warehouse = WarehouseDAO.get_by_id(warehouse_id=warehouse_slip.source_warehouse_id)
        for slip_detail in warehouse_slip.slip_details:
            self.edit_stock(warehouse=warehouse, 
                            slip_detail=slip_detail, 
                            updater=lambda stock,quantity: setattr(stock,'quantity',stock.quantity - quantity))
        # warehouse.save_all(warehouse.stocks)