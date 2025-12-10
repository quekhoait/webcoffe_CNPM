from eapp import db
from eapp.models import WarehouseSlipDetail
class WarehouseSlipDAO():
    @staticmethod
    def create_warehouse_slip(warehouse_slip, warehouse_slip_details):
        db.session.add(warehouse_slip)
        db.session.flush()
        print(warehouse_slip.id)
        for detail in warehouse_slip_details:
            wearehouse_slip_detail = WarehouseSlipDetail(**detail)
            wearehouse_slip_detail.warehouse_slip_id = warehouse_slip.id
            db.session.add(wearehouse_slip_detail)
        
        db.session.commit()

        return warehouse_slip