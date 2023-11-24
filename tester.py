from utils.config import *
from library.mysql_load import *

cfg = Configs()
conf = cfg.get_data_config()
print(conf)

mys = Mysql()
#op = mys.execute_mysql_query("create table test2(id int)")
df = mys.get_data_from_mysql("select * from test2")
print(df)