from ..models.user import User
from ..models.recommendation import Recommendation
class UserService:
    @staticmethod
    def get_all_user():
        return User.get_all_users()
    
    @staticmethod
    def get_user_id(user_id):
        return User.get_user_by_id(user_id)
    
    @staticmethod 
    def get_recommentdation(user_id , doctor_id ):
        return Recommendation.get_chat_by_id(user_id , doctor_id)
    