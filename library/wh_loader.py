import pandas as pd

class WHLoader:
    def __init__(self):
        pass

    def load_states_to_wh(self, mys, df):
        drop_table_query = "drop table if exists states"
        create_table_query = """
            create table if not exists states(
                map_state varchar(100),
                existing_state varchar(100)
                )
            """
        op = mys.load_data_to_mysql_alchemy(df = df, drop_table_query=drop_table_query, create_table_query=create_table_query, table_name="states")
        #print(df.size)        
        return op    

    def load_agg_trans_to_wh(self, mys, df):
        drop_table_query = "drop table if exists agg_trans"
        create_table_query = """
            create table if not exists agg_trans(
                states varchar(500),
                years varchar(20),
                quarters varchar(10),
                transaction_name varchar(500),
                transaction_count bigint,
                transaction_amount float
                )
            """
        op = mys.load_data_to_mysql_alchemy(df = df, drop_table_query=drop_table_query, create_table_query=create_table_query, table_name="agg_trans")
        #print(df.size)        
        return op
    
    def load_agg_users_to_wh(self, mys, df):    
        drop_table_query = "drop table if exists agg_users"
        create_table_query = """
            create table if not exists agg_users(
                states varchar(500),
                years varchar(20),
                quarters varchar(10),
                brands varchar(500),
                transaction_count bigint,
                percentage float
                )
            """
        op = mys.load_data_to_mysql_alchemy(df = df, drop_table_query=drop_table_query, create_table_query=create_table_query, table_name="agg_users")
        return op

    def load_map_trans_to_wh(self, mys, df):    
        drop_table_query = "drop table if exists map_trans"
        create_table_query = """
            create table if not exists map_trans(
                states varchar(500),
                years varchar(20),
                quarters varchar(10),
                districts varchar(500),
                transaction_count bigint,
                transaction_amount float
                )
            """
        op = mys.load_data_to_mysql_alchemy(df = df, drop_table_query=drop_table_query, create_table_query=create_table_query, table_name="map_trans")
        print(df.size)
        return op

    def load_map_users_to_wh(self, mys, df):    
        print(df.size)
        drop_table_query = "drop table if exists map_users"
        create_table_query = """
            create table if not exists map_users(
                states varchar(500),
                years varchar(20),
                quarters varchar(10),
                districts varchar(500),
                registered_users bigint,
                app_opens bigint
                )
            """
        op = mys.load_data_to_mysql_alchemy(df = df, drop_table_query=drop_table_query, create_table_query=create_table_query, table_name="map_users")
        #print(df.size)
        return op

    def load_top_trans_to_wh(self, mys, df):    
        drop_table_query = "drop table if exists top_trans"
        create_table_query = """
            create table if not exists top_trans(
                states varchar(500),
                years varchar(20),
                quarters varchar(10),
                districts varchar(500),
                transaction_count bigint,
                transaction_amount float
                )
            """
        op = mys.load_data_to_mysql_alchemy(df = df, drop_table_query=drop_table_query, create_table_query=create_table_query, table_name="top_trans")
        return op

    def load_top_users_to_wh(self, mys, df):    
        drop_table_query = "drop table if exists top_users"
        create_table_query = """
            create table if not exists top_users(
                states varchar(500),
                years varchar(20),
                quarters varchar(10),
                districts varchar(500),
                registered_users bigint
                )
            """
        op = mys.load_data_to_mysql_alchemy(df = df, drop_table_query=drop_table_query, create_table_query=create_table_query, table_name="top_users")
        return op


