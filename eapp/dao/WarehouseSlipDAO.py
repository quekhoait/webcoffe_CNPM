from eapp import db
from eapp.models import WarehouseSlipDetail
class WarehouseSlipDAO():
    @staticmethod
    def create_warehouse_slip(warehouse_slip, warehouse_slip_details):
        try:
            db.session.add(warehouse_slip)
            db.session.flush()
            
            for detail in warehouse_slip_details:
                slip_detail = WarehouseSlipDetail(
                    warehouse_slip_id=warehouse_slip.id,
                    ingredient_id=detail['ingredient_id'],
                    quantity=detail['quantity']
                )
                db.session.add(slip_detail)
            db.session.commit()
            return warehouse_slip
        except Exception as ex:
            db.session.rollback()
            print(f"Lỗi khi tạo phiếu kho warehouseslip: {ex}")
            return None