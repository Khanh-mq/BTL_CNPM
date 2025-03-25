from ..models.doctor import Doctor
from ..models.appointment import Appointment
from ..models.recommendation import Recommendation
class DoctorService:
    @staticmethod
    def create_doctor(data : dict):
        return Doctor.create_doctor(data)
    
    
    @staticmethod 
    def get_all_doctor():
        return Doctor.get_doctor_all()

    @staticmethod
    def get_appointment_by_id_doctor(id):
        return Doctor.get_appointment(id)

    
    @staticmethod 
    def acccept_status_service(doctor_id, appointment_ids):
        #  khi accept thi tao cho một cái recommentdation_userid và doctor id
        return  Appointment.accept_status(doctor_id , appointment_ids)
    
    @staticmethod
    def content_recommendation_service(user_id , doctor_id , content):
        Recommendation.create_recommentdaton(doctor_id , user_id)
        return Recommendation.contentRecommendation(user_id ,  doctor_id ,  content)
    
    '''doctor'''
    @staticmethod
    def register(data):
        return Doctor.register(data)
    
    
    @staticmethod
    def login(data):
        email =  data['email']
        password = data['password']
        doctor =  Doctor.login(email , password)
        return doctor