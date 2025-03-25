from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Dict
from .database import Database
from flask_bcrypt import Bcrypt

class Base(DeclarativeBase):
    pass 

class DoctorORM(Base):
    __tablename__ = "Doctors"
    
    doctor_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    specialty: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
    
    def _asdict(self) -> dict:
        return {
            'doctor_id': self.doctor_id, 
            'name': self.name, 
            'specialty': self.specialty,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class Doctor:
    '''Hàm tạo bác sĩ'''
    @staticmethod 
    def create_doctor(doctor_data: Dict) -> int:
        """Tạo một bác sĩ mới.
        - Trả về `doctor_id` nếu thành công.
        - Trả về `-1` nếu thất bại."""
        
        db = Database()
        engine = db.get_connection()
        if not engine:
            print("Không thể kết nối đến database.")
            return -1 
        
        try:
            
            with Session(engine) as session:
                if Doctor.check_Doctor(session , doctor_data.get('email')):
                    print('doctor  da ton tai')
                    return -1
                new_doctor = DoctorORM(
                    name=doctor_data.get('name'),
                    specialty=doctor_data.get('specialty'),
                    email=doctor_data.get('email'),
                    password=Doctor.set_password(doctor_data.get('password')),  # Hash password
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                session.add(new_doctor)
                session.commit()  # Lưu vào database
                return new_doctor.doctor_id
        
        except SQLAlchemyError as e:
            print(f"Lỗi khi thêm bác sĩ: {str(e)}")
            return -1
    
    
    
    @staticmethod
    def check_Doctor(session : Session , email : str) -> bool:
        return session.query(DoctorORM).filter_by(email = email).first() is not None

    
    @staticmethod
    def get_doctor_all():
        db  = Database()
        engine = db.get_connection()
        if not engine:
            print("Không thể kết nối đến database.")
            return -1 
        
        try:
            
            with Session(engine) as session:
                doctors =  session.query(DoctorORM).all()
                return [{'doctor_id':doctor.doctor_id , 
                         'name':doctor.name , 
                         'specialty':doctor.specialty} for doctor in doctors ]
        except SQLAlchemyError as e:
            print(f"Lỗi khi thêm bác sĩ: {str(e)}")
            return -1
        
        
    @staticmethod
    def register(doctor_data):
        ''' Đăng ký tài khoản mới '''
        db = Database()
        engine = db.get_connection()
        if not engine:
            return {'error': 'Không thể kết nối database'}
        try:
            with Session(engine) as session:
                ''' Kiểm tra tài khoản tồn tại '''
                existing_doctor = session.query(DoctorORM).filter_by(email=doctor_data.get('email')).first()
                if existing_doctor:
                    return {'error': "Email đã được sử dụng"}
                ''' Tạo doctor mới '''
                new_doctor = DoctorORM(
                    name=doctor_data.get('name'),
                    email=doctor_data.get('email'),
                    password=Doctor.set_password(doctor_data.get('password')),  # Hash password
                    specialty=doctor_data.get('specialty'),
                    created_at = datetime.now(),
                    updated_at = ""
                )
                session.add(new_doctor)
                session.commit()
                return {'success': "Đăng ký thành công", 'doctor_id': new_doctor.doctor_id}
        except SQLAlchemyError as e:
            session.rollback()
            return {'error': f'Lỗi database: {str(e)}'}

    @staticmethod
    def login( email , password):
        db = Database()
        engine =  db.get_connection()
        if not engine:
            return {"error": "Không thể kết nối đến database"}
        try:
            with Session(engine) as session:
                doctor = session.query(DoctorORM).filter(DoctorORM.email ==  email).first()
                if not doctor:
                    return {"error" : "email khong ton tai"}
                if not Doctor.check_password(doctor.password , password):
                    return {'error' : "mat khau khong dung"}
            
                return doctor.doctor_id
        except SQLAlchemyError as e :
            return {'error' : f"loi data :{str(e)}"}
    
    
    @staticmethod
    def set_password(password: str) -> str:
        return Bcrypt().generate_password_hash(password).decode('utf-8')
    
    
    @staticmethod
    def check_password(hashed_password: str, password: str) -> bool:
        return Bcrypt().check_password_hash(hashed_password, password)

    