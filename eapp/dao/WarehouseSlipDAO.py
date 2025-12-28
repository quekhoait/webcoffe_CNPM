from dataclasses import dataclass
from typing import Optional
from eapp import app, db
from eapp.models import WarehouseSlipDetail
from eapp.models.WarehouseSlip import WarehouseSlip

@dataclass
class WarehouseSlipFilter:
    warehouse_id : Optional[str] = None

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
    
    @staticmethod
    def list(params : WarehouseSlipFilter = None):
        try:
            query = WarehouseSlip.query
            return query.all()
        except Exception as ex:
            app.logger.error('Lỗi khi lấy danh sách warehouse slip')
            return []
        

    def get_by_id(slip_id):
        try:
            query = WarehouseSlip.query
            return query.get(slip_id)
        except Exception as ex: 
            app.logger.error('Lỗi khi lấy phiếu kho theo id', exc_info=True)
            return None