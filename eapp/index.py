from flask import session
from flask_login import current_user
from flask_socketio import SocketIO, emit, join_room
from eapp import app,db
# from eapp.models. import Product
# from eapp.models.BaseModel import BaseModel
# from eapp.models.CategoryModel import Categories
# from eapp.dao.Product import add_product

socketio = SocketIO(app, async_mode='eventlet')


@socketio.on('connect')
def handle_connect():
    print(f"{current_user.name} vừa đăng nhập")

@socketio.on('join_warehouse')
def handle_join(data):
    print(f"{current_user.name} đã đăng nhập vào kho {session.get('warehouse_id',1)}" )
    join_room(session.get('warehouse_id',1))

@socketio.on('send')
def handle_send(data):
    print(data['msg'])
    emit('receive', {'msg': data['msg']}, room=data['warehouse_id'])



if __name__ == '__main__':
    with app.app_context():
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)