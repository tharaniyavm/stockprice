# database.py
import mysql.connector
import pandas as pd
from mysql.connector import Error
from sqlalchemy import create_engine
from config import ConnectionInfo

class DatabaseManager:
    @staticmethod
    def get_connection():
        try:
            conn = mysql.connector.connect(
                host=ConnectionInfo.HOST,
                user=ConnectionInfo.USER,
                password=ConnectionInfo.PASSWORD,
                database=ConnectionInfo.DATABASE,
                port=ConnectionInfo.PORT
            )
            return conn
        except Error as e:
            print(f"Error: {e}")
            return None
        


def df_to_mysql(df, table_name):
    """Sends a pandas DataFrame to a MySQL table."""
    
    # 1. Create the SQLAlchemy Engine URL
    # Format: mysql+mysqlconnector://user:password@host:port/database
    url = (f"mysql+mysqlconnector://{ConnectionInfo.USER}:{ConnectionInfo.PASSWORD}"
           f"@{ConnectionInfo.HOST}:{ConnectionInfo.PORT}/{ConnectionInfo.DATABASE}")
    
    engine = create_engine(url)

    try:
        # 2. Upload the data
        # if_exists options: 'fail', 'replace' (drops table first), 'append'
        df.to_sql(
            name=table_name, 
            con=engine, 
            if_exists='replace', 
            index=False  # Set to True if you want to keep the DF index
        )
        print(f"Success: '{table_name}' table updated.")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        
    finally:
        engine.dispose() # Clean up connection pool

# Example Usage:
# my_data = pd.DataFrame({'name': ['Alice'], 'age': [25]})
# df_to_mysql(my_data, 'employees')
    
