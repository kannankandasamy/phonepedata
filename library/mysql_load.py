import mysql.connector
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
from utils.config import *

class Mysql:
    """
    Mysql class to get mysql connection object and does data processing using mysql

    - Stores data into mysql methods are there to store line by line and bulk
    - Retreives data from mysql using pandas dataframe and lists
    """
    def __init__(self):
        cfg = Configs()
        conf = cfg.get_data_config()
        self.conf = conf

    def get_mysql_connection(self):
        """
        Gets mysql regular connection to do row by row processing
        """
        mysql_user = self.conf['mysql_user']
        mysql_pwd = self.conf['mysql_pwd']
        mysql_host = self.conf['mysql_host']
        mysql_db = self.conf['mysql_db']
        cnx = mysql.connector.Connect(user=mysql_user,password=mysql_pwd, host=mysql_host, database=mysql_db)
        return cnx
    
    def get_mysql_alchemy_engine(self):
        """
        Gets mysql alchemy engine connection to do dataframe level bulk processing
        Passwords are coming thru data.conf
        """
        engine = sqlalchemy.create_engine("mysql://{0}:{1}@{2}:{3}/{4}".format(
            self.conf['mysql_user'],
            self.conf['mysql_pwd'],
            self.conf['mysql_host'],
            self.conf['mysql_port'],
            self.conf['mysql_db']))
        con = engine.connect()
        self.engine = engine
        return engine

    def execute_mysql_query(self, query):
        """
        Executes a sql query and returns success or failed, this is primarily to do ddl operations
        """
        try:
            cnx = self.get_mysql_connection()
            with cnx.cursor() as cursor:
                result = cursor.execute(query)
                #rows = cursor.fetchall()
            cnx.commit()
            cnx.close()
            return "SUCCESS"
        except Exception as ex:
            print(ex)
            return "FAILED"        

    def execute_mysql_query_with_values(self, query, values):
        """
        Executes a sql query with values associated to it
        """
        try:
            cnx = self.get_mysql_connection()
            with cnx.cursor() as cursor:
                result = cursor.execute(query, values)
                #rows = cursor.fetchall()
            cnx.commit()
            cnx.close()
            return "SUCCESS"
        except:
            return "FAILED"              




    def get_data_from_mysql(self, query):
        """
        Gets data from mysql as a pandas dataframe by running a query
        """
        try:
            cnx = self.get_mysql_connection()
            df = pd.read_sql(query, cnx)
            cnx.close()
            return df
        except:
            return "FAILED"        
        

    def load_data_to_mysql_alchemy(self, **connection):
        """
        Gets channel details from mongodb and loads into mysql as bulk
        """
        
        drop_channel_query =  connection["create_table_query"]   
        create_channel_query = connection["create_table_query"]

        op = self.execute_mysql_query(drop_channel_query)
        op = self.execute_mysql_query(create_channel_query)

        try:
            eng = self.get_mysql_alchemy_engine()
            op = connection["df"].to_sql(name='channels', con=eng,if_exists='append',index=False)
            print(op)
        except Exception as ex:
            return "FAILED" + str(ex)
        return "SUCCESS ROWS "+str(op)                   
    

      
