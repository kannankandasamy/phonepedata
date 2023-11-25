from utils.config import *
from library.mysql_load import *
from library.data_loader import *
from library.wh_loader import *

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
        wh = WHLoader()

        df = dl.get_agg_trans()
        op = wh.load_agg_trans_to_wh(mys, df)
        print(op)


        df = dl.get_agg_users()
        op = wh.load_agg_users_to_wh(mys, df)      
        print(op)
    
        df = dl.get_map_trans()
        op = wh.load_map_trans_to_wh(mys, df)
        print(op)             

        df = dl.get_map_users()
        op = wh.load_map_users_to_wh(mys, df)
        print(op)    

        df = dl.get_top_trans()
        op = wh.load_top_trans_to_wh(mys, df)
        print(op)          

        df = dl.get_top_users()
        op = wh.load_top_users_to_wh(mys, df)
        print(op)    