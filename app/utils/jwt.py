import datetime 
from flask import request
from functools import wraps 
from flask import request , jsonify
from flask_socketio import disconnect
import jwt
SECRET_KEY = "3749274823h73ry39874944"
class Sec :
    @staticmethod
    def generate_token(user_id : int ) -> str:
        payload =  {
            "user_id" :user_id, 
            "exp" : datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        return jwt.encode(payload , SECRET_KEY , algorithm="HS256" )
    
    
    @staticmethod 
    def verify_token(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            #  lấy token trong authorization hoac o trong 
            token = request.headers.get("Authorization") 
            if not token :
                return jsonify({'error' :"token khong ton tai"}) , 401
            
            
            
            try:
                decoded = jwt.decode(token , SECRET_KEY , algorithms=['HS256'])
                request.user_id  = decoded["user_id"]
                request.doctor_id =  decoded["user_id"]
            except jwt.ExpiredSignatureError:
                return jsonify({'erorr' : "token da het han"}) , 401 
            except jwt.InvalidTokenError:
                return jsonify({'error':"token khong hop le "}) , 401 
            return f(*args, **kwargs)
        return decorated
            