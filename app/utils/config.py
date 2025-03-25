"""ket noi data base """
from dotenv import load_dotenv
import os
load_dotenv()
class Config:
    SQL_SERVER =  os.getenv('SQL_SERVER')
    DEBUG = os.getenv('DEBUG' , 'True').lower() ==  'true'



config =  Config()
