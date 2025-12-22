#nhận request từ giao diện post, get
from flask import app, jsonify, render_template, request, session

from eapp.dao import ProductDao
from eapp.dao.InvoiceDAO import InvoiceDAO
from eapp.services import InvoiceService
from eapp.services.inventory.InventoryValidator import InventoryValidator
from eapp.models.Invoice import InvoiceStatusEnum
from eapp.controllers import index



def list(filehtml):
    def view_function():
        params = request.args.to_dict()
        products = ProductDao.list(params)
        return render_template(filehtml,
                               products=products)

    return view_function


def get_product():
    params = request.args.to_dict()
    dishes = ProductDao.list(params)
    product_makeable_map = InventoryValidator.get_product_makeable_map(dishes, index.get_current_warehouse())
    return render_template('page/menu_product_item.html',
                           products=dishes,
                           product_makeable_map=product_makeable_map)


def delete_invoice():
    invoice_id = request.get_json().get('invoice_id')
    invoice=InvoiceDAO.get_by_id(int(invoice_id))
    if not invoice_id:
        return jsonify({"success": False, "message": "Missing invoice_id"}), 400
    try:
        # Giả sử warehouse_id có thể lấy từ session hoặc mặc định
        warehouse_id = request.args.get("warehouse_id", 1)
        if invoice.invoice_status != InvoiceStatusEnum.PENDING:
            return jsonify({"status": "error", "message": f"Lỗi"})
        InvoiceService.InvoiceService.update_invoice_status(invoice, InvoiceStatusEnum.CANCELLED,
                                                            warehouse_id=warehouse_id)
        return jsonify({"status": "success", "message": f"Đơn hàng hủy thành công."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



