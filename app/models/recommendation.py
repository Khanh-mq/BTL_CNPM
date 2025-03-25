from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import Dict
from .database import Database
from ..models.doctor import DoctorORM
from sqlalchemy import or_ ,  and_

class Base(DeclarativeBase):
    pass 
class RecommendationORM(Base):
    __tablename__  = "Recommendations"
    
    
    recommendation_id : Mapped[int] =  mapped_column( primary_key= True, autoincrement= True , )
    user_id : Mapped[int] =  mapped_column()
    doctor_id : Mapped[int] =  mapped_column()
    recommendation_type : Mapped[str] =  mapped_column()
    content :Mapped[str] =  mapped_column()
    created_at : Mapped[datetime] = mapped_column()
    
    
    
    def _asdict(self)-> dict:
        return {
            'recommendation_id' : self.recommendation_id, 
            'user_id' : self.user_id, 
            'doctor_id' :self.doctor_id , 
            'recommendation_type' : self.recommendation_type , 
            'content' :self.content , 
            'created_at' :self.created_at
        }
''' su dung chat socket de nhan tu van truc tiep cho bac si voi benh nhan  thong qua chat
nguoi dung  hoac bac si se lay token cua minh va lay id cua nguoi kia de vao thuc hien doan chat voi nhau'''
class Recommendation:
    @staticmethod
    def get_chat_by_id(user_id , doctor_id ):
        db = Database()
        engine =  db.get_connection()
        if not engine:
            print('noi ket noi data')
            return -1 
        try :
            with Session(engine)  as session:
                result =  session.query(RecommendationORM).filter(RecommendationORM.user_id ==  user_id , RecommendationORM.doctor_id== doctor_id).all()
                if not result:
                    print('khong co du lieu')
                    return -1
                return [row._asdict() for row in result]
        except SQLAlchemyError as e:
            print(f'loi data base : {str(e)}')
            return -1
        #  dong data base 
        engine.Close()
    
    
    @staticmethod 
    def contentRecommendation(user_id ,  doctor_id ,  content):
        '''doctor viet khuyen cao cho user sau khi kham benh ve
        doctor_id lay trong token 
        user_id lay  tren url 
        '''
        db = Database()
        engine =  db.get_connection()
        if not engine:
            print('noi ket noi data')
            return -1 
        try :
            with Session(engine)  as session:
                #  kiem tra ton tai trong database
                result =  session.query(RecommendationORM).filter(
                    RecommendationORM.user_id ==  user_id,
                    RecommendationORM.doctor_id ==  doctor_id,
                ).first()
                if not result:
                    print('recommentdation khong ton tai ')
                    return -1
                result.content =  content.get('content')
                result.recommendation_type = content.get('recommendation_type')
                result.created_at =  datetime.now()
                session.commit()
                return result.recommendation_id
        except SQLAlchemyError as e :
            session.rollback()
            print(f'loi khi cap viet recommentdation : {str(e)}')
            return -1
                

    @staticmethod
    def create_recommentdaton(doctor_id , user_id):
        db = Database()
        engine = db.get_connection()
        if not engine:
            print("khong ket noi duoc data base")
            return -1
        try:
            with Session(engine) as session:
                #  kiem tra xem co recommentdaiton exsits  
                result =  session.query(RecommendationORM).filter(
                    RecommendationORM.doctor_id ==  doctor_id,
                    RecommendationORM.user_id ==  user_id,
                ).first()
                if not result:
                    print("recomemntdation khong ton tai")
                    new_recommentdation = RecommendationORM(
                        user_id =  user_id,
                        doctor_id =doctor_id,
                        recommendation_type ="",
                        content ="",
                        created_at =  datetime.now(),
                    )
                    session.add(new_recommentdation)
                    session.commit()
                    return new_recommentdation.recommendation_id
        except SQLAlchemyError as e:
            print(f'loi data base{str(e)}')
            return -1
                    
            
                
    
    
            

    
    