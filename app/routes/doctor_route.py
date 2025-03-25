from flask import Blueprint ,  request , jsonify
from ..services.doctor_service import DoctorService
from ..services.appointment_service import Appointment
from ..utils.jwt import Sec
doctor_bp = Blueprint('doctor' , __name__)

'''
bác sĩ có thể lấy danh sách bệnh nhân đặt lịch cho mình
kiểm duyệt trạng thái lịch khám cho bệnh nhân
'''
@doctor_bp.route('/doctor' , methods =  ['POST'])
def create_doctor():
    doctor_data = request.json
    result = DoctorService.create_doctor(doctor_data)
    return jsonify(result) , 201 if result != -1 else 400




@doctor_bp.route('/doctor/get_appointment_tomorrow' , methods=['GET'])
@Sec.verify_token
def get_appointment_tomorrow_by_id_doctor():
    doctor_data = request.doctor_id
    status = request.args.get("status", 0) 
    result = Appointment.get_appointment_tomorow(doctor_data , status)
    return jsonify(result) , 201  if result != -1 else 400

@doctor_bp.route('/doctor/login' , methods = ['POST'])
def login():
    data =  request.get_json()
    print(data)
    response = DoctorService.login(data)
    token =  Sec.generate_token(response)
    return jsonify({
        "user" : response,
        "token" : token     
    }),200

@doctor_bp.route('/doctor/register' , methods =  ['POST'])
def register():
    data =  request.get_json()
    response = DoctorService.register(data)
    return jsonify(response), 201 if 'success' in response else 400

@doctor_bp.route('/doctor/accepct_status' , methods = ['POST'])
@Sec.verify_token
def status():
    appointment_id = request.get_json()
    print(appointment_id)
    
    doctor_id =  request.doctor_id
    result = DoctorService.acccept_status_service(doctor_id , appointment_id)
    return jsonify(result) , 201 if result !=  -1 else 401
    


@doctor_bp.route("/doctor/recommentdation/content" , methods=['POST'])
@Sec.verify_token
def content_recomemtdatin():
    user_id = request.args.get('user_id')
    doctor_id =  request.doctor_id
    content =  request.get_json()
    result =  DoctorService.content_recommendation_service(user_id , doctor_id , content)
    return jsonify(result) , 201 if result != -1 else 400
