#nhận request từ giao diện post, get
from flask import app, jsonify, render_template, request, session

from eapp.dao import ProductDao
from eapp.services.inventory.InventoryValidator import InventoryValidator




def list(filehtml):
    def view_function():
        params = request.args.to_dict()

        products = ProductDao.list(params)
        return render_template(filehtml, 
                               products=products,
                               product_status_map=InventoryValidator.get_product_makeable_map(products,session.get('warehouse_id',1)))
    return view_function


def get_product():
    params = request.args.to_dict()
    dishes = ProductDao.list(params)
    return jsonify([d.to_dict() for d in dishes]), 200






