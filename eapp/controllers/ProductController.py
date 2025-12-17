#nhận request từ giao diện post, get
from flask import app, jsonify, render_template, request

from eapp.dao import ProductDao




def list(filehtml):
    def view_function():
        params = request.args.to_dict()

        products = ProductDao.list(params)
        print(products)
        return render_template(filehtml, products=products)

    return view_function


def get_product():
    params = request.args.to_dict()
    dishes = ProductDao.list(params)
    return jsonify([d.to_dict() for d in dishes]), 200


def get_product_by_status():
    invoice_status = request.args.get("invoice_status")
    payment_status = request.args.get("payment_status")
    prod_list=ProductDao.get_product_by_status_dao(invoice_status, payment_status)
    result = []
    for p in prod_list:
        result.append({
            "invoice_id": p.id
        })
    return jsonify(result)



