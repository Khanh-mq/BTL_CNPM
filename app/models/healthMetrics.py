from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Dict

from app.models.database import Database

from ..ML.preditct_ml import ML

class Base(DeclarativeBase):
    pass 
class HealthMetricsORM(Base):
    __tablename__ ='HealthMetrics'
    
    
    metric_id :  Mapped[int] =  mapped_column(primary_key=True , autoincrement= True)
    user_id : Mapped[int] =  mapped_column() 
    weight : Mapped[float] = mapped_column()
    height :Mapped[float] =  mapped_column()
    blood_pressure :Mapped[str] =  mapped_column()
    heart_rate : Mapped[int] = mapped_column()
    blood_sugar : Mapped[float] = mapped_column()
    created_at :Mapped[datetime] =  mapped_column()
    updated_at : Mapped[datetime] = mapped_column()
    age : Mapped[int] =  mapped_column()
    typed : Mapped[str] =  mapped_column()
    gender: Mapped[str] = mapped_column()
    
    
    def _asdict(self)->dict:
        return {
            'metric_id' : self.metric_id , 
            'gender': self.gender,
            'user_id' : self.user_id , 
            'weight' : self.weight, 
            'height' :self.height,
            'blood_pressure' :self.blood_pressure,
            'heart_rate' :self.heart_rate,
            'blood_sugar' : self.blood_sugar,
            'age' : self.age , 
            'created_at' :self.created_at,
            'updated_at' : self.updated_at,
            'typed' :self.typed
        }
        
class HealthMetrics:
        
    def check_health(session : Session , user_id : int)-> bool :
        return session.query(HealthMetricsORM).filter_by(user_id =user_id).first() is not None
    @staticmethod
    def create_health(user_id : int , health_data)->int:
        """ tao mot heal moi 
        moi user chi co mot health 
        thanh cong tra ve  ma int cua use da tao 
        that bai thogn bao  tra ve -1 """
        db = Database()
        engine =  db.get_connection()
        if not engine:
            print("Không thể kết nối đến database.")
            return -1 
        try : 
            with Session(engine) as session:
                if HealthMetrics.check_health(session ,user_id):
                    print('heald da ton tai')
                    return -1
                health_data.update({
                    "user_id": user_id,
                    "created_at": datetime.now(),
                    "updated_at": None,
                })
                new_health = HealthMetricsORM(**health_data)
                session.add(new_health)
                session.commit()
                return new_health.user_id
        except   SQLAlchemyError as e:
            print(f'loi khi tao  health {str(e)}')
            return -1
        
        
        
        
    #  cap nhat health cho user
    @staticmethod
    def update_health(user_id: int, health_data: dict) -> int:
        """Cập nhật health bằng cách tạo bản ghi mới để lưu lịch sử."""
        try:
            with Session(Database().get_connection()) as session:
                # Lấy bản ghi gần nhất của user
                latest_health = (
                    session.query(HealthMetricsORM)
                    .filter(HealthMetricsORM.user_id == user_id)
                    .order_by(HealthMetricsORM.updated_at.desc())
                    .first()
                )

                if not latest_health:
                    print("Lỗi: Không tìm thấy health record.")
                    return -1

                # Gộp dữ liệu mới và cũ
                new_health_data = {**latest_health.__dict__, **health_data}

                # Loại bỏ các trường không cần thiết
                new_health_data.pop("_sa_instance_state", None)
                new_health_data.pop("metric_id", None)

                # Cập nhật thời gian mới
                new_health_data.update({
                    # "created_at": datetime.now(),  # Ghi lại thời điểm tạo mới
                    "updated_at": datetime.now()   # Cập nhật thời gian mới nhất
                })

                # Tạo bản ghi mới
                new_health = HealthMetricsORM(**new_health_data)
                session.add(new_health)
                session.commit()
                return user_id

        except SQLAlchemyError as e:
            session.rollback()
            print(f"Lỗi khi cập nhật health: {str(e)}")
            return -1
        
    @staticmethod 
    def get_health_by_user_id(user_id)-> dict:
        '''' nguoi dung va bac si co quyen lay  ho so benh kham cua benh nhan'''
        db = Database()
        engine =  db.get_connection()
        if not engine :
            return {'error' : f'khong ket noi duoc database'}
        try:
            with Session(engine)as session:
                user =  session.query(HealthMetricsORM).filter(HealthMetricsORM.user_id ==  user_id).order_by(HealthMetricsORM.updated_at.desc()).first()
                if not user :
                  return {'error' : f' khong tim thay ho  so suc khoe cua {user_id} '}
                    
                return user._asdict()
        except SQLAlchemyError as e:
            return {'error' : f'loi database: {str(e)}'}
    
    
    @staticmethod 
    def get_health_all()-> list[dict]:
        """Lấy tất cả người dùng từ database."""
        db = Database()
        engine = db.get_connection()  # Gọi phương thức get_connection() đã định nghĩa
        if not engine:
            return [{'error': 'Không thể kết nối database'}]

        try:
            with Session(engine) as session:
                health = session.query(HealthMetricsORM).all()
                return [health._asdict() for health in health]
        except SQLAlchemyError as e:
            return [{'error': f'Lỗi database: {str(e)}'}]




                     
