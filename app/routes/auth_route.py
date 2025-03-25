from flask import Blueprint , request , jsonify
from ..services.auth_service import AuthService
from ..services.auth_service import AuthService
from ..utils.jwt import Sec
#  dang nhap va dang ki tai khoan cho user
auth = Blueprint('auth' , __name__)

@auth.route('/user/register' , methods =  ['POST'])
def register():
    data =  request.get_json()
    response = AuthService.register(data)
    return jsonify(response), 201 if 'success' in response else 400



@auth.route('/login' , methods = ["POST"])
def login():
    data =  request.get_json()
    print(data)
    response = AuthService.login(data)
    token =  Sec.generate_token(response)
    return jsonify({
        "user" : response,
        "token" : token     
    }),200
    