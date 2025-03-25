# database.py
import urllib
from sqlalchemy import create_engine

class Database:
    def __init__(self):
        self.server = 'DESKTOP-2L7A1VS\\SQLEXPRESS'
        self.database = 'QuanLiSucKhoe'
        self.username = 'maikhanh'
        self.password = 'khanh2004'
        self.driver = 'ODBC Driver 17 for SQL Server'
        self.engine = None

    def get_connection(self):
        """Trả về engine của SQLAlchemy."""
        if self.engine is None:
            try:
                params = urllib.parse.quote_plus(
                    f"DRIVER={{{self.driver}}};"
                    f"SERVER={self.server};"
                    f"DATABASE={self.database};"
                    f"UID={self.username};"
                    f"PWD={self.password}"
                )
                self.engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
            except Exception as e:
                print(f"Không thể kết nối: {str(e)}")
                return None
        return self.engine