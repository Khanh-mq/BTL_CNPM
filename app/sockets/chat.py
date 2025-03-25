from flask import Blueprint, request
from flask_socketio import emit, join_room, leave_room
from ..utils.jwt import Sec
# Tạo Blueprint cho chat
chat_bp = Blueprint('chat', __name__)

# Dictionary để theo dõi các phòng và session
rooms = {}

# Định nghĩa route HTTP (tùy chọn, nếu bạn cần)
# @chat_bp.route('/chat')
# def chat_index():
#     return "Chat endpoint"
@Sec.verify_token
# Hàm đăng ký các sự kiện SocketIO
def init_socketio(socketio):
    # Xử lý khi client kết nối
    @socketio.on('connect')
    def handle_connect():
        room = request.args.get('room')
        if not room:
            print("Lỗi: Không có room được cung cấp")
            return
        join_room(room)
        if room not in rooms:
            rooms[room] = set()
        rooms[room].add(request.sid)
        print(f"Client {request.sid} đã tham gia phòng {room}. Danh sách: {rooms[room]}")
        emit('status', {'message': f"Đã tham gia phòng {room}", 'room': room}, room=request.sid)

        print(f"Client {request.sid} đã kết nối")

    # Xử lý khi client tham gia phòng
    @socketio.on('join_room')
    def handle_join_room(data):
        room = data.get('room')
        if not room:
            print("Lỗi: Không có room được cung cấp")
            return
        join_room(room)
        if room not in rooms:
            rooms[room] = set()
        rooms[room].add(request.sid)
        print(f"Client {request.sid} đã tham gia phòng {room}. Danh sách: {rooms[room]}")
        emit('status', {'message': f"Đã tham gia phòng {room}", 'room': room}, room=request.sid)

    # Xử lý khi client rời phòng
    @socketio.on('leave_room')
    def handle_leave_room(data):
        room = data.get('room')
        if room and request.sid in rooms.get(room, set()):
            leave_room(room)
            rooms[room].remove(request.sid)
            print(f"Client {request.sid} đã rời phòng {room}. Danh sách: {rooms[room]}")
            emit('status', {'message': f"Đã rời phòng {room}", 'room': room}, room=request.sid)
        else:
            print(f"Client {request.sid} không trong phòng {room}")

    # Xử lý khi client gửi tin nhắn
    @socketio.on('chat_message')
    def handle_chat_message(data):
        room = request.args.get('room')
        message = data.get('message')
        if not room or not message:
            print("Lỗi: room hoặc message không hợp lệ")
            return
        print(f"Nhận từ client {request.user_id} trong phòng {room}: {message}")
        # Gửi tin nhắn tới tất cả client trong phòng, trừ người gửi
        socketio.emit('chat_message', {'message': message, 'sender_sid': request.user_id}, room=room, include_self=False)
        print(f"Đã gửi tin nhắn tới phòng {room}. Danh sách: {rooms.get(room, 'Không có phòng')}")