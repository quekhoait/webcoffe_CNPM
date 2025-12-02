from eapp.dao import RuleDAO
from eapp.models import Rule
from eapp.services.RuleService import RuleService


class InvoiceService:
    
    # tổng tiền item trong hóa đơn
    @staticmethod
    def calculate_total(invoice : dict) -> float:
        return sum(item['quantity'] * item['price'] for item in invoice.values())
    
    # thêm món vào hóa đơn
    @staticmethod
    def add_item_to_invoice(invoice : dict, item_data : dict) -> dict:
        item_id = str(item_data.get('id'))
        bonus_quantity = int(item_data.get('bonus_quantity', 1))
        
        if item_id in invoice:
            if item_data.get('is_set_quantity'):
                invoice[item_id]['quantity'] = bonus_quantity
            else:
                invoice[item_id]['quantity'] += bonus_quantity

        else:
            invoice[item_id] = {
                "id": item_id,
                "name": item_data.get('name'),
                "price": item_data.get('price'),
                "quantity": bonus_quantity
            }

        return invoice
    
    @staticmethod
    def remove_item_from_invoice(invoice: dict, item_id: str) -> dict:
        del invoice[item_id]
        return invoice
    
    # tính luôn phí dịch vụ
    @staticmethod
    def calculate_final_total(total: float) -> float:
        service_fee = RuleService.calulate_service_fee(total)
        final_total = total + service_fee
        return final_total