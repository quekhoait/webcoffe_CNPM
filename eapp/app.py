from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')

# Trang chính, có thể truyền username
@app.route('/')
def index():
    username = request.args.get('username', 'User')
    return render_template('demo.html', username=username)

# Khi client gửi message
@socketio.on('send_message')
def handle_message(data):
    username = data['username']
    message = data['message']
    room = data['room']
    
    # Gửi về tất cả trong room
    emit('receive_message', {'username': username, 'message': message}, room=room)

# Khi client join room
@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('receive_message', {'username': 'System', 'message': f"{data['username']} has joined the room."}, room=room)

# Khi client leave room
@socketio.on('leave')
def on_leave(data):
    room = data['room']
    leave_room(room)
    emit('receive_message', {'username': 'System', 'message': f"{data['username']} has left the room."}, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
