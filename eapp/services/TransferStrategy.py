from sqlalchemy import desc
from eapp.dao.WarehouseDAO import WarehouseDAO
from eapp.models import Stock, Warehouse, WarehouseSlip, WarehouseSlipDetail
from eapp.services.SlipStrategy import SlipStrategy


class TransferStrategy(SlipStrategy):
    def update_stock(self, warehouse_slip: WarehouseSlip):
        src_warehouse = WarehouseDAO.get_by_id(warehouse_id=warehouse_slip.source_warehouse_id)
        dst_warehouse = WarehouseDAO.get_by_id(warehouse_id=warehouse_slip.destination_warehouse_id)

        for slip_detail in warehouse_slip.slip_details:
            self.edit_stock(warehouse=src_warehouse,
                            slip_detail=slip_detail,
                            updater=lambda stock,quantity: setattr(stock,'quantity',stock.quantity - quantity))
            
            self.edit_stock(warehouse=dst_warehouse,
                            slip_detail=slip_detail,
                            updater=lambda stock,quantity: setattr(stock,'quantity',stock.quantity + quantity))
            
        src_warehouse.save_all(src_warehouse.stocks)
        dst_warehouse.save_all(dst_warehouse.stocks)

            
        
               