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
        print(df.size)

        df = dl.get_agg_users()
        print(df.size)

        df = dl.get_map_trans()
        print(df.size)

        df = dl.get_map_users()
        print(df.size)

        df = dl.get_top_trans()
        print(df.size)

        df = dl.get_top_users()
        print(df.size)
