from flask import Blueprint ,  request , jsonify
from flask_socketio import SocketIO , join_room , leave_room , send
from datetime  import datetime


chat_bp = Blueprint('chatxx' , __name__)

@chat_bp.route("/send" , methods=['POST'])
def send_message():
    data =  request.get_json()
    room_id = data['room_id']
    username = data['username']
    message = data['message']
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    
    SocketIO.emit('message', {'user': username, 'message': message, 'timestamp': timestamp}, room=room_id)
    return jsonify({'status': 'success', 'message': 'Tin nhắn đã được gửi.'})
