from hmac import new
from eapp.dao import PaymentDao
from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.models import InvoiceDetail, Rule
from eapp.models import Invoice
from eapp.models.Invoice import INVOICE_STATUS_LABEL, InvoiceStatusEnum, PaymentMethod
from eapp.models.Payment import PaymentStatus
from eapp.services.RuleService import RuleService
from eapp import app, db
from eapp.services.inventory.InventoryFacade import InventoryFacade
from eapp.services.inventory.RecipeService import RecipeService
from eapp.services.inventory.StockService import StockService



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
            invoice.invoice_status = InvoiceStatusEnum.PENDING

            invoice_details = []
            for detail in invoice_data.get('invoice_items', []):
                invoice_details.append(
                    InvoiceDetail(
                        product_id=int(detail['product_id']),
                        quantity=detail['quantity'],
                        price=detail['price']
                    )
                )

            #flush
            InvoiceDAO.create(invoice=invoice,invoice_details=invoice_details)
            
            #cập nhật reserveđ
            StockService.reserve_stock_for_invoice(
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
            'insufficient_ingredients': None,
            'effected_products': None
        }
        method = "offline"
        if invoice.payment_method == PaymentMethod.MOMO:
            method = "online"

        valid_status, message = InvoiceService.invoice_validator(invoice.invoice_status,new_status,method)    
        if not valid_status:
            result['success'] = False
            result['message'] = message
            return result

        try:
            #xử lý hóa đơn sang in progress
            if new_status == InvoiceStatusEnum.IN_PROGRESS:
                rs = InventoryFacade.start_processing_invoice(invoice,warehouse_id)
                invoice.invoice_status = InvoiceStatusEnum.IN_PROGRESS
                if rs['success']:
                    result.update({
                        'success': True,
                        'message': 'Xác thực thành công, hóa đơn đang được xử lý',
                        'invoice': invoice
                    })
                else:
                    result.update({
                    'message': 'Nguyên liệu không đủ cho hóa đơn',
                    'insufficient_ingredients': rs['insufficient_ingredients'],
                    'effected_products' : rs['effected_products']    
                    })

            elif new_status == InvoiceStatusEnum.COMPLETED:
                invoice.invoice_status = InvoiceStatusEnum.COMPLETED
                result.update({
                    'success': False,
                    'message': 'Hóa đơn đã hoàn thành',
                    'invoice': invoice
                })

            elif new_status == InvoiceStatusEnum.CANCELLED:
                InventoryFacade.cancel_processing_invoice(invoice,warehouse_id)
                payments = PaymentDao.get_by_invoice_id(invoice.id)
                if payments:
                    for payment in payments:
                        payment.status = PaymentStatus.failed
                invoice.invoice_status = InvoiceStatusEnum.CANCELLED
                result.update({
                    'success': True,
                    'message': 'Hủy hóa đơn thành công',
                    'invoice': invoice
                })

            else:
                result['message'] = 'Trạng thái hóa đơn không hợp lệ'

            db.session.commit()
        except Exception as ex:
            db.session.rollback()
            app.logger.error(f"Lỗi khi xử lý hóa đơn sang IN_PROGRESS: {str(ex)}",exc_info=True)
            result.update({
                'success' : False,
                'message' : 'Lỗi hệ thống khi xử lý hóa đơn'
            })
        return result
    
    @staticmethod
    def invoice_validator(current_status:InvoiceStatusEnum, new_status:InvoiceStatusEnum,method='offline'):
        if current_status in [InvoiceStatusEnum.CANCELLED,InvoiceStatusEnum.COMPLETED]:
            return False, f"Hóa đơn đã {INVOICE_STATUS_LABEL[method][current_status]}, không thể thay đổi"
        
        change_status_map = {
            InvoiceStatusEnum.PENDING: [InvoiceStatusEnum.IN_PROGRESS,InvoiceStatusEnum.CANCELLED],
            InvoiceStatusEnum.IN_PROGRESS: [InvoiceStatusEnum.COMPLETED]
        }
        if new_status in change_status_map.get(current_status,[]):
            return True, "Cho phép"

        return False, f"Không thể chuyển hóa đơn từ đã {INVOICE_STATUS_LABEL[method][current_status]} sang {INVOICE_STATUS_LABEL[method][new_status]}"

    