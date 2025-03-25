from sklearn.preprocessing  import StandardScaler
import joblib
import pandas as pd 
import os 
class ML:
    @staticmethod 
    def Chuan_Hoa(data):
        model_path = os.path.join(os.getcwd(), "app", "ML", "modelSVM.pkl")
        loaded_SVM = joblib.load(r'app\ML\modelSVM.pkl')
        data =  pd.DataFrame(data=data , columns=['Gender' , 'Height' , 'Weight'])  
        scaler  =  StandardScaler()
        Train_X  = pd.read_csv(r'app\ML\train_x.csv')
        scaler.fit(Train_X)
        data_read_std = scaler.transform(data)
        
        
        return  loaded_SVM.predict(data_read_std)[0]

        