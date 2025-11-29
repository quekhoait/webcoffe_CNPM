#nhận request từ giao diện post, get
from flask import app, jsonify, render_template, request

from eapp.dao import ProductDao



# @app.route('/api/dish', methods=['get'])
def list():
    """
    params
        id
        dish_category_id
        name
    """
    params = request.args.to_dict()
    # re2=DishDAO.list(params)
    # result = [d.to_dict() for d in DishDAO.list(params)]
    dishes = DishDAO.list(params)
    # import pdb
    # pdb.set_trace
    # return jsonify(result),200


    return render_template("staff/dish_item.html",dishes = dishes)

