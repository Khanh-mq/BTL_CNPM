from flask import Blueprint ,  request , jsonify
from ..services.user_service import UserService
from ..services.doctor_service import DoctorService
from ..utils.jwt import Sec
from ..services.health_service import HealthService
from ..services.appointment_service import AppointmentService

user_bp = Blueprint('user' , __name__)
''' dang ki  , dang nhap 
    chinh sua tai khoan mat khau
    xem danh sach bac si
    nhan tu van suc khoe 
    dat lịch hen 
    chinh sua thong tin sức khỏe
    xem lịch hẹn 
'''
#  dang ki user 

#  xem danh sach bac sy
@user_bp.route('/user/get_doctor_all' ,  methods = ['GET'])
def get_doctor_all():
    get_all = DoctorService.get_all_doctor()
    return jsonify(get_all), 200 if get_all != None else 400

@user_bp.route('/user', methods=['GET'])
def get_users():
    """ api lay danh sach nguoi dung"""
    users =  UserService.get_all_user()
    return jsonify(users) , 200 


@user_bp.route('/user/health' , methods = ['GET'])
@Sec.verify_token
def get_health_by_id():
    user_id =  request.user_id
    print(user_id)
    health =  HealthService.get_health_by_user_id(user_id)
    if 'error' in health :
        return jsonify({'error' : health['error']}) , 404 
    return jsonify(health) , 200 


@user_bp.route('/user/create_health' , methods=['POST'])
@Sec.verify_token
def create_health():
    user_id =  request.user_id
    health_data =  request.json
    result =  HealthService.create_health(user_id , health_data)
    return jsonify(result) , 201 if result != -1 else 400



@user_bp.route('/user/update_health' , methods=['PUT'])
@Sec.verify_token
def update_health():
    user_id =  request.user_id
    data =  request.json
    result = HealthService.update_health_by_user_id(user_id , data)
    return jsonify(result) , 201 if result != -1 else 400 

@user_bp.route('user/get_doctor' ,  methods =  ['GET'])
@Sec.verify_token
def get_all_doctor():
    result  = DoctorService.get_all_doctor()
    return jsonify(result), 200 if get_all_doctor != None else 400


#  tao cuoc hen cho user
@user_bp.route('/user/appointment/create_appointment' ,  methods=['POST'])
@Sec.verify_token
def create_appointment():
    data = request.get_json()
    resutl = AppointmentService.create_appointment(data)
    return jsonify(resutl) , 201 if resutl != -1 else 400
    


@user_bp.route('/user/appointment/get_appointment' , methods = ['GET'])
@Sec.verify_token
def get_appointmetn():
    #  vi  dau vao phai la 1 dict  nen viec lay ra phai gawn cho no 1 dict 
    data_id  =  request.user_id
    status =  request.args.get('status')
    data = {"user_id" : data_id}
    result = AppointmentService.get_appointment_by_id(data , status)
    return jsonify(result) , 200  if result != -1 else 400 


@user_bp.route('/user/appointment/update_appointment' , methods = ['PUT'])
@Sec.verify_token
def update_appointment():
    user_id =  request.user_id
    data =  request.get_json()
    result =  AppointmentService.update_appointment(user_id , data) 
    return jsonify(result) , 200  if result != -1 else 400

@user_bp.route('/user/<int:user_id>' , methods = ['GET'])
@Sec.verify_token
def get_user_id(user_id):
    user =  UserService.get_user_id(user_id)
    if 'error' in user :
        return jsonify({'error' : user['error']}) , 404 
    return jsonify(user) , 200 


@user_bp.route('/user/recommentdation' ,  methods =  ['GET'])
@Sec.verify_token
def get_recommendation():
    user_id =  request.user_id
    doctor_id  =  request.args.get('doctor_id')
    result = UserService.get_recommentdation(user_id , doctor_id)
    return jsonify(result) , 201 if result != -1 else 400
