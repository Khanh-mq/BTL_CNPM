from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Optional
from .database import Database  # Import lớp Database đã sửa
from flask_bcrypt import Bcrypt
# Định nghĩa Base cho ORM
class Base(DeclarativeBase):
    pass

# Định nghĩa ánh xạ ORM cho bảng Users
class UserORM(Base):
    __tablename__ = "Users"

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    
    

    def _asdict(self) -> Dict:
        """Chuyển đổi đối tượng UserORM thành từ điển."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            
            'password': self.password, 
            
        }

# Lớp User sử dụng ORM
class User:
    def __init__(self, user_id=None, name=None, email=None, password=None, gender=None ):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.gender = gender
        
        # self.create_at = timezone
        # self.update_at = timezone 

    def _asdict(self) -> Dict:
        """Chuyển đổi đối tượng User thành từ điển."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'gender': self.gender,
            'password': self.password,
            
                
        }
    @staticmethod
    def get_all_users() -> List[Dict]:
        """Lấy tất cả người dùng từ database."""
        db = Database()
        engine = db.get_connection()  # Gọi phương thức get_connection() đã định nghĩa
        if not engine:
            return [{'error': 'Không thể kết nối database'}]

        try:
            with Session(engine) as session:
                users = session.query(UserORM).all()
                return [user._asdict() for user in users]
        except SQLAlchemyError as e:
            return [{'error': f'Lỗi database: {str(e)}'}]

    
    @staticmethod
    def update_user(user_data: Dict) -> int:
        """
        Cập nhật thông tin người dùng trong database.
        Chỉ cập nhật các trường được cung cấp trong user_data.
        Trả về user_id nếu thành công, -1 nếu thất bại.
        """
        db = Database()
        engine = db.get_connection()
        if not engine:
            return -1

        user_id = user_data.get('user_id')
        if not user_id:
            print("Lỗi: user_id không được cung cấp.")
            return -1

        try:
            with Session(engine) as session:
                # Tìm người dùng dựa trên user_id
                user = session.query(UserORM).filter(UserORM.user_id == user_id).first()
                if not user:
                    print(f"Lỗi: Không tìm thấy người dùng với user_id {user_id}")
                    return -1

                # Cập nhật chỉ các trường có trong user_data
                if 'name' in user_data:
                    user.name = user_data['name']
                if 'email' in user_data:
                    user.email = user_data['email']
                if 'password' in user_data:
                    user.password = user_data['password']
                if 'gender' in user_data:
                    user.gender = user_data['gender']
               

                session.commit()
                return user.user_id
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Lỗi khi cập nhật người dùng: {str(e)}")
            return -1
        
        
        
    def update_user(user_data : Dict) -> int :
        """cập nhật thong tin ngươi dungf trong database 
        trar về uẻid neu thanh cong 1 , that bai la -1"""
        db = Database()
        engine =  db.get_connection()
        if not engine:
            return -1 
        user_id = user_data.get('user_id')
        if not user_id:
            print('loi user khogn duoc cung cap')
            return -1
        try:
            with Session(engine)  as session:
                user = session.query(UserORM).filter(UserORM.user_id ==  user_id).first()
                if not user:
                    print(f'lỗi khong tìm thấy user_id : {user_id}')
                    return -1
                user.name =  user_data.get('name' , user.name)
                user.email =  user_data.get('email', user.email)
                user.password =  user_data.get('password' , user.password)
                user.gender =  user_data.get('gender' , user.gender)
                session.commit()
                return user.user_id
        except SQLAlchemyError as e :
            session.rollback()
            print(f'loi khi cập nhật người dùng : {str(e)}')
            return -1

    @staticmethod
    def get_user_by_id(user_id : int ) -> Dict:
        db = Database()
        engine = db.get_connection()
        if not engine :
            return {'error' : f'khong ket noi duoc database'}
        try:
            with Session(engine)as session:
                user =  session.query(UserORM).filter(UserORM.user_id ==  user_id).first()
                if not user :
                  return {'error' : f'loi database: {str(e)}'}
                    
                return user._asdict()
        except SQLAlchemyError as e:
            return {'error' : f'loi database: {str(e)}'}

    @staticmethod
    def set_password(password: str) -> str:
        return Bcrypt().generate_password_hash(password).decode('utf-8')
    
    
    @staticmethod
    def check_password(hashed_password: str, password: str) -> bool:
        return Bcrypt().check_password_hash(hashed_password, password)

    
    @staticmethod
    def register(user_data):
        ''' Đăng ký tài khoản mới '''
        db = Database()
        engine = db.get_connection()
        if not engine:
            return {'error': 'Không thể kết nối database'}
        try:
            with Session(engine) as session:
                ''' Kiểm tra tài khoản tồn tại '''
                existing_user = session.query(UserORM).filter_by(email=user_data.get('email')).first()
                if existing_user:
                    return {'error': "Email đã được sử dụng"}
                ''' Tạo user mới '''
                new_user = UserORM(
                    name=user_data.get('name'),
                    email=user_data.get('email'),
                    password=User.set_password(user_data.get('password')),  # Hash password
                    gender=user_data.get('gender'),
                    
                )
                session.add(new_user)
                session.commit()
                return {'success': "Đăng ký thành công", 'user_id': new_user.user_id}
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
                user = session.query(UserORM).filter(UserORM.email ==  email).first()
                if not user:
                    return {"error" : "email khong ton tai"}
                if not User.check_password(user.password , password):
                    return {'error' : "mat khau khong dung"}
            
                return user.user_id
        except SQLAlchemyError as e :
            return {'error' : f"loi data :{str(e)}"}