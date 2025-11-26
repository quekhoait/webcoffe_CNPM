from flask import app, jsonify, request

from eapp.dao.DishDAO import DishDAO


# @app.route('/api/dish', methods=['get'])
def list():
    """
    params
        id
        dish_category_id
        name
    """
    params = request.args.to_dict()
    re2=DishDAO.list(params)
    result = [d.to_dict() for d in DishDAO.list(params)]
    
    import pdb
    pdb.set_trace
    return jsonify(result),200