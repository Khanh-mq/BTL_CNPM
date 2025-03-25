from flask import Flask
from .routes.user_route  import user_bp
from .models.database import Database
from .models.user import User
from .routes.doctor_route import doctor_bp
from .routes.health_route import health_bp
from .routes.auth_route import auth
from flask_socketio import SocketIO 


from .sockets.chat import chat_bp, init_socketio


app =  Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*" , async_mode='eventlet')

app.register_blueprint(user_bp , url_prefix = '/api')
app.register_blueprint(doctor_bp , url_prefix =  '/api')
# app.register_blueprint(health_bp , url_prefix =  '/api')
app.register_blueprint(auth , url_prefix = '/api')
app.register_blueprint(chat_bp , url_prefix = '/api')
#  goi lenh chat



# init_socketio(socketio)
# Sử dụng class với thông tin của bạn
if __name__ == "__main__":
    # Tạo bảng nếu chưa tồn tại
    # db = Database()
    # engine = db.get_connection()
    # if engine:
    #     Base.metadata.create_all(engine)

    # Lấy tất cả người dùng
    # users = User.get_all_users()
    # for user in users:
    #     print(user)

    
    """khoi tao server"""
    # app.run(debug= True , host='0.0.0.0' , port=5000 )
    socketio.run(app , debug=True , host='0.0.0.0' , port=5000)
    
    
    