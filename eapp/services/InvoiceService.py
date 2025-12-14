from eapp.dao import PaymentDao
from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.dao.InvoiceDetailDAO import InvoiceDetailDAO
from eapp.models import InvoiceDetail, Rule
from eapp.models import Invoice
from eapp.models.Invoice import InvoiceStatusEnum, PaymentMethod
from eapp.services.InventoryService import InventoryService
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
        invoice,
        invoice_items: {
            product_id: {
                id,
                quantity,
                price
            }
        }
    """
    
    """
        lưu chi tiết invoice_items, phụ phí hiện tại (rule)
        tính tổng tạm, final
    """
    @staticmethod
    def create_invoice(invoice_data: dict) -> Invoice:
        invoice = Invoice()
        
        invoice.order_code = PaymentDao.generate_order_code()
        invoice.customer_id = invoice_data.get('customer_id', None)     
        invoice.staff_id = invoice_data.get('staff_id',None)
        invoice.cashier_id = invoice_data.get('cashier_id', None)           
        invoice.payment_method = PaymentMethod.CASH
        invoice.invoice_status = InvoiceStatusEnum.PENDING
        invoice.subtotal = InvoiceService.calculate_total(invoice_data.get('invoice_items', []))
        invoice.extra_fee_total = RuleService.calulate_service_fee(invoice.subtotal)
        invoice.final_total = invoice.subtotal + invoice.extra_fee_total

        InvoiceDAO.create(invoice)

        invoiceDetails = []
        for item in invoice_data.get('invoice_items', []).values():
            detail = InvoiceDetail()
            detail.invoice_id = invoice.id
            detail.product_id = int(item['id'])
            detail.quantity = item['quantity']
            detail.price = item['price']
            invoiceDetails.append(detail)
        
        print(InvoiceDetailDAO.create(invoiceDetails))

        return invoice
    

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


    