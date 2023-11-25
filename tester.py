from utils.config import *
from library.mysql_load import *
from library.data_loader import *

class PhonepeAnalytics:
    if __name__=="__main__":
        cfg = Configs()
        conf = cfg.get_data_config()
        print(conf)

        mys = Mysql()
        #op = mys.execute_mysql_query("create table test2(id int)")
        df = mys.get_data_from_mysql("select * from test2")
        print(df)

        dl = DataLoader()
        df = dl.get_agg_trans()
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
        print(df.size)
        print(op)


        df = dl.get_agg_users()
        print(df.size)
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
        print(df.size)
        print(op)        

        df = dl.get_map_trans()
        print(df.size)
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
        print(op)             

        df = dl.get_map_users()
        print(df.size)

        df = dl.get_top_trans()
        print(df.size)

        df = dl.get_top_users()
        print(df.size)
