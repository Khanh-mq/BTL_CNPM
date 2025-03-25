from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session 
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Dict
from .database import Database
from ..models.doctor import DoctorORM
from sqlalchemy import or_ ,  and_ , update
from datetime import datetime, timedelta


class Base(DeclarativeBase):
    pass 
class AppointmentORM(Base):
    __tablename__  = "Appointments"
    
    
    
    appointment_id:Mapped[int] =  mapped_column(primary_key=True ,  autoincrement=True)
    user_id :Mapped[int] = mapped_column()
    doctor_id :Mapped[int] =  mapped_column()
    notes: Mapped[str] =  mapped_column()
    status:Mapped[int] = mapped_column()
    appointment_time : Mapped[datetime] =  mapped_column()
    created_at : Mapped[datetime] = mapped_column()
    updated_at : Mapped[datetime] = mapped_column()
    
    
    
    def _asdict(self):
        return {
            'appointment_id': self.appointment_id,
            'user_id' : self.user_id,
            'doctor_id' : self.doctor_id,
            'notes': self.notes,
            'status':self.status,
            'appointment_time' : self.appointment_time,
            'created_at' : self.created_at , 
            'updated_at' : self.updated_at
        }
class Appointment:
    
    
    
    @staticmethod
    def create_appointment(data):
        '''tao cuoc hen giua user vs doctor''' 
        db = Database()
        engine =  db.get_connection()
        #  kiem tra bác sĩ tồn tại hay không 
        if not engine:
            print("khogn the ket noi data base")
            return -1 
        try:
            with Session(engine) as session:
                #  kiem tra bac si co ton tai hay khong 
                doctor  = session.query(DoctorORM).filter_by(doctor_id = data.get('doctor_id')).first()
                if not doctor:
                    print("bac si khogn ton tai")
                    return -1
                #  kiem tra xem cuoc hen do ton tai hay chua 
                existing_appointment = session.query(AppointmentORM).filter_by(
                user_id=data.get("user_id"),
                doctor_id=data.get("doctor_id"),
                appointment_time=data.get("appointment_time")
                ).first()
            if existing_appointment:
                print("Cuộc hẹn đã tồn tại")
                return -1
            #  tao cuoc hop moi 
            new_appointment = AppointmentORM(
                user_id = data.get('user_id'),
                doctor_id = data.get('doctor_id'),
                appointment_time = data.get("appointment_time"), 
                notes =  data.get("notes"),
                status = data.get("status",  0),
                created_at = datetime.utcnow(), 
                updated_at = data.get('updated_at')
            )
            session.add(new_appointment)
            session.commit()
            return new_appointment.appointment_id
        except SQLAlchemyError as e:
            print(f"khogn the ket noi : {str(e)}")
    
    
    
    '''xem cac cuoc hen cua user'''
    @staticmethod
    def get_appointment_id(data , status):
        db =  Database()
        engine = db.get_connection()
        if not engine :
            print("noi ket noi data  base")
            return -1 
        try :
            with Session(engine) as session:
                #  kiem tra xem appointment do co ton tai hay khong 
                result =  session.query(AppointmentORM).filter(
                    or_(
                        AppointmentORM.user_id == data.get('user_id'),
                        AppointmentORM.doctor_id ==  data.get('doctor_id')
                    ),AppointmentORM.status == status
                ).all()
                return [appointment._asdict()for appointment in result]
            
        except SQLAlchemyError as e :
            print(f"loi khong co cuoc hen : {str(e)}")
            return -1
        
        
    @staticmethod
    def update_appointment(user_id , data):
        db = Database()
        engine =  db.get_connection()
        if not engine:
            print("khong ket noi duoc data base")
            return -1
        try :
            with Session(engine ) as session:
                #  kiem tra xem  co ton tai hay khong 
                result =  session.query(AppointmentORM).filter(
                    AppointmentORM.user_id == user_id,
                    AppointmentORM.appointment_id ==  data.get('appointment_id') , 
                    AppointmentORM.status == 0
                ).first()
                if not result:
                    print("appointment khong ton tai hoac da duoc duyet")
                    return -1 
                for key , values in data.items():
                    setattr(result , key , values)
                result.updated_at = datetime.now()
                print(f'gia tri result  la : {result}')
                session.commit()
                return user_id
        except SQLAlchemyError as e:
            session.rollback()
            print(f'loi khi cap nhat appointment : {str(e)}')
            return -1
                
    
    @staticmethod
    def get_appointment_tomorow(id_doctor , status = 0 ):
        db = Database()
        engine = db.get_connection()
        if not engine:
            print("khong ket noi duoc data base")
            return -1
        try:
            with Session(engine)  as session:
                tomorrow = (datetime.today() + timedelta(days=1)).date()

            # Truy vấn danh sách cuộc hẹn của bác sĩ vào ngày mai
            if status == 0:
                result = session.query(AppointmentORM).filter(
                AppointmentORM.doctor_id == id_doctor,
                AppointmentORM.appointment_time == tomorrow,
                
            ).all()
            elif status !=  0:
                result = session.query(AppointmentORM).filter(
                AppointmentORM.doctor_id == id_doctor,
                AppointmentORM.appointment_time == tomorrow,
                AppointmentORM.status == status
            ).all()
            
            return [appointment._asdict()for appointment in result]
        except  AttributeError as e:
            print(f'khong the lay duoc appointment vao ngay mai(tomorrow)')
            return -1 
    
    
    
    @staticmethod
    def accept_status(doctor_id, appointment_ids):
        db = Database()
        engine = db.get_connection()
        if not engine:
            print("Không kết nối được database")
            return -1
        try:
            
            with Session(engine) as session:
                stmt = update(AppointmentORM).where(
                    and_(AppointmentORM.appointment_id.in_(appointment_ids.get('appointment_id')), # Danh sách số nguyên
                    AppointmentORM.doctor_id == doctor_id,
                    AppointmentORM.status == 0)
                ).values(status=1, updated_at=datetime.now())

                session.execute(stmt)
                session.commit()
                
                result =  session.query(AppointmentORM).filter(
                    AppointmentORM.appointment_id ==  appointment_ids
                ).first()
                
                return result
        except Exception as e:
            print(f"Lỗi: {e}")
            return {"error": str(e)}, 500
    
    
    