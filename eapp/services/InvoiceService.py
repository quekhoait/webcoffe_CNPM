from hmac import new
from eapp.dao import PaymentDao
from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.models import InvoiceDetail, Rule
from eapp.models import Invoice
from eapp.models.Invoice import InvoiceStatusEnum, PaymentMethod
from eapp.services.InventoryService import InventoryService
from eapp.services.RuleService import RuleService
from eapp import app, db


class InvoiceService:
    
    # tổng tiền item trong hóa đơn
    @staticmethod
    def calculate_total(invoice : list) -> float:
        return sum(item['quantity'] * item['price'] for item in invoice)
    
    @staticmethod
    def is_invalid_value(currentValue, newValue, isSetQuantity):
        try:
            value = int(newValue)
        except (ValueError, TypeError):
            return "Yêu cầu nhập vào 1 số nguyên"
        
        if isSetQuantity and value <= 0:
            return "Yêu cầu nhập số lượng lớn hơn 0"

        if (currentValue + value) <= 0:
            return "Số lượng tăng thêm phải lớn hơn 0"
        
        return None
    # thêm món vào hóa đơn

    @staticmethod
    def calculate_new_quantity(invoice: dict, item_data: dict) -> int:
      
        item_id = str(item_data.get('id'))
        bonus_quantity = int(item_data.get('bonus_quantity', 1))
        current_quantity = invoice.get(item_id, {}).get('quantity', 0)

        if item_data.get('is_set_quantity'):
            return bonus_quantity
        else:
            return current_quantity + bonus_quantity

    @staticmethod
    def add_item_to_invoice(invoice : dict, item_data : dict, new_quantity: int) -> dict:
        item_id = str(item_data.get('id'))
        bonus_quantity = int(item_data.get('bonus_quantity', 1))

        item_id = str(item_data.get('id'))

        if item_id in invoice:
            invoice[item_id]['quantity'] = new_quantity
        else:
            invoice[item_id] = {
                "product_id": item_id,
                "name": item_data.get('name'),
                "price": item_data.get('price'),
                "quantity": new_quantity
            }

        return invoice
    

    @staticmethod
    def remove_item_from_invoice(invoice: dict, item_id: str) -> dict:
        del invoice[item_id]
        return invoice
    
    # tính tổng gồm luôn phí dịch vụ
    @staticmethod
    def calculate_final_total(total: float) -> float:
        service_fee = RuleService.calulate_service_fee(total)
        final_total = total + service_fee
        return final_total
    


    """
        customer_id,
        staff_id,
        cashier_id,
        payment_method,
        invoice,
        invoice_items: [
            {
                product_id,
                quantity,
                price
            }
        ]
    """
    
    """
        lưu chi tiết invoice_items, phụ phí hiện tại (rule)
        tính tổng tạm, final
    """
    @staticmethod
    def create_invoice(invoice_data: dict, warehouse_id=None, used_stock=None) -> Invoice:
        try:
            invoice = Invoice()
            invoice.order_code = PaymentDao.generate_order_code()
            invoice.customer_id = invoice_data.get('customer_id', None)     
            invoice.staff_id = invoice_data.get('staff_id',None)
            invoice.cashier_id = invoice_data.get('cashier_id', None)           
            invoice.payment_method = invoice_data.get('payment_method')
            invoice.subtotal = InvoiceService.calculate_total(invoice_data.get('invoice_items', []))
            invoice.extra_fee_total = RuleService.calulate_service_fee(invoice.subtotal)
            invoice.final_total = invoice.subtotal + invoice.extra_fee_total

            InvoiceDAO.save(invoice)
            db.session.flush()  

            invoice_details = []
            for detail in invoice_data.get('invoice_items', []):
                invoice_details.append(
                    InvoiceDetail(
                        invoice_id=invoice.id,
                        product_id=int(detail['product_id']),
                        quantity=detail['quantity'],
                        price=detail['price']
                    )
                )
            InvoiceDAO.save_details(invoice_details)

            if warehouse_id and used_stock:
                InventoryService.reserve_stock_for_invoice(
                    invoice=invoice,
                    warehouse_id=warehouse_id,
                    used_stock=used_stock
                )

            db.session.commit()
            return invoice

        except Exception as ex:
            db.session.rollback()
            app.logger.exception(str(ex))
            raise Exception("Xảy ra lỗi khi tạo hóa đơn")

    

    def update_invoice_status(invoice: Invoice, new_status: InvoiceStatusEnum, warehouse_id: int = None):
        result = {
            'success': False,
            'message': '',
            'invoice': None,
            'insufficient_ingredients': None
        }

        if new_status == InvoiceStatusEnum.IN_PROGRESS:
            invoice.invoice_status = InvoiceStatusEnum.IN_PROGRESS
            rs = InventoryService.invoice_process(invoice,warehouse_id)
            if rs['success']:
                result.update({
                    'success': True,
                    'message': 'Hóa đơn đang được xử lý',
                    'invoice': invoice
                })
            else:
                result.update({
                'message': 'Nguyên liệu không đủ cho hóa đơn',
                'insufficient_ingredients': rs['insufficient_ingredients']
                })

        elif new_status == InvoiceStatusEnum.COMPLETED:
            if invoice.invoice_status != InvoiceStatusEnum.IN_PROGRESS:
                result['message'] = 'Hóa đơn chưa được xử lý'
            else:
                invoice.invoice_status = InvoiceStatusEnum.COMPLETED
                result.update({
                    'success': True,
                    'message': 'Hóa đơn đã hoàn thành',
                    'invoice': invoice
                })

        elif new_status == InvoiceStatusEnum.CANCELLED:
            if invoice.invoice_status == InvoiceStatusEnum.COMPLETED:
                result['message'] = 'Không thể hủy hóa đơn đã hoàn thành'
            else:
                invoice.invoice_status = InvoiceStatusEnum.CANCELLED
                result.update({
                    'success': True,
                    'message': 'Hủy hóa đơn thành công',
                    'invoice': invoice
                })

        else:
            result['message'] = 'Trạng thái hóa đơn không hợp lệ'

        if result['invoice']:
            result['invoice'].save()
        return result


    