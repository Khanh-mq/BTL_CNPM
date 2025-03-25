from app.ML.preditct_ml import ML
from ..models.healthMetrics import HealthMetrics
import pandas as pd 
class HealthService:
    @staticmethod
    def create_health(user_id , data) -> int:
        gender , height , weight  = data.get('gender') , data.get('height') , data.get('weight')
        data_predict = pd.DataFrame([[gender, height, weight]] , columns=['Gender' , 'Height' , 'Weight'])
        typed =  ML.Chuan_Hoa(data_predict)
        print(typed)
        data['typed'] =  typed
        print(data)
        return HealthMetrics.create_health(user_id , data)
    
    @staticmethod
    def get_health_all():
        return HealthMetrics.get_health_all();
    
    
    @staticmethod
    def get_health_by_user_id(user_id):
        return HealthMetrics.get_health_by_user_id(user_id)
    
    
    @staticmethod
    def update_health_by_user_id(user_id ,data):
        #  lay data gender , height , weight để chuyển vào mô hình học máy 
        gender , height , weight  = data.get('gender') , data.get('height') , data.get('weight')
        data_predict = pd.DataFrame([[gender, height, weight]] , columns=['Gender' , 'Height' , 'Weight'])
        typed =  ML.Chuan_Hoa(data_predict)
        print(typed)
        data['typed'] =  typed
        print(data)
        return HealthMetrics.update_health(user_id , data)