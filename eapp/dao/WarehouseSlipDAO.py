from eapp import db
from eapp.models import WarehouseSlipDetail
class WarehouseSlipDAO():
    @staticmethod
    def create_warehouse_slip(warehouse_slip, warehouse_slip_details):
        db.session.add(warehouse_slip)
        db.session.flush()

        for detail in warehouse_slip_details:
            slip_detail = WarehouseSlipDetail(
                warehouse_slip_id=warehouse_slip.id,
                ingredient_id=int(detail['ingredient_id']),
                quantity=float(detail['quantity'])
            )
            db.session.add(slip_detail)
        return warehouse_slip
