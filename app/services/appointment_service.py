from ..models.appointment import Appointment

class AppointmentService:
    @staticmethod
    def create_appointment(data):
        return Appointment.create_appointment(data)
    
    
    @staticmethod 
    def get_appointment_by_id(data ,  status):
        return Appointment.get_appointment_id(data ,  status)
    
    @staticmethod 
    def update_appointment(user_id , data):
        return Appointment.update_appointment(user_id , data)