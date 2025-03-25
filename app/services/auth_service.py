from ..models import User 
class AuthService:
    ''' user'''
    @staticmethod
    def register(data):
        return User.register(data)
    
    
    @staticmethod
    def login(data):
        email =  data['email']
        password = data['password']
        user =  User.login(email , password)
        return user
    