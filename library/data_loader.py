import os
import pandas as pd
import json

class DataLoader:
    def __init__(self):
        pass

    def get_correct_states(self):
        #df = pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")
        df=pd.read_csv("C:/kannan/code/phonepedata/data/states/map_state.csv")
        return df

    def get_agg_trans(self):
        aggpath = "C:/kannan/code/phonepedata/data/aggregated/transaction/country/india/state/"
        agg_tran_list = os.listdir(aggpath)
        #print(agg_tran_list)
        cols1 = {"states":[],"years":[],"quarters":[],"transaction_name":[],"transaction_count":[], "transaction_amount":[]}
        for s in agg_tran_list:
            cur = aggpath+s+"/"
            agg_yr_list = os.listdir(cur)
            for y in agg_yr_list:
                cur_y = cur+y+"/"
                agg_file_list = os.listdir(cur_y)
                for f in agg_file_list:
                    cur_f = cur_y+f
                    data = open(cur_f,"r")
                    json_data = json.load(data)
                    for rec in json_data["data"]["transactionData"]:
                        name = rec["name"]
                        count = rec["paymentInstruments"][0]["count"]
                        amount = rec["paymentInstruments"][0]["amount"]
                        cols1["transaction_name"].append(name)
                        cols1["transaction_count"].append(count)
                        cols1["transaction_amount"].append(amount)
                        cols1["states"].append(s)
                        cols1["years"].append(y)
                        cols1["quarters"].append(f.strip(".json"))
        df = pd.DataFrame(cols1)
        return(df)        
                

    def get_agg_users(self):
        agg_user_path = "C:/kannan/code/phonepedata/data/aggregated/user/country/india/state/"
        agg_user_list = os.listdir(agg_user_path)
        #print(agg_tran_list)
        user_cols1 = {"states":[],"years":[],"quarters":[],"brands":[],"transaction_count":[], "percentage":[]}
        for s in agg_user_list:
            cur = agg_user_path+s+"/"
            agg_yr_list = os.listdir(cur)
            for y in agg_yr_list:
                cur_y = cur+y+"/"
                agg_file_list = os.listdir(cur_y)
                for f in agg_file_list:
                    cur_f = cur_y+f
                    data = open(cur_f,"r")
                    json_data = json.load(data)
                    try:
                        for rec in json_data["data"].get("usersByDevice"):
                            brand = rec["brand"]
                            count = rec["count"]
                            percentage = rec["percentage"]
                            user_cols1["brands"].append(brand)
                            user_cols1["transaction_count"].append(count)
                            user_cols1["percentage"].append(percentage)
                            user_cols1["states"].append(s)
                            user_cols1["years"].append(y)
                            user_cols1["quarters"].append(f.strip(".json"))
                    except:
                        pass
        df = pd.DataFrame(user_cols1)
        return(df)   

    def get_map_trans(self):
        mappath = "C:/kannan/code/phonepedata/data/map/transaction/hover/country/india/state/"
        map_tran_list = os.listdir(mappath)
        #print(agg_tran_list)
        map_tran_cols = {"states":[],"years":[],"quarters":[],"districts":[],"transaction_count":[], "transaction_amount":[]}
        for s in map_tran_list:
            cur = mappath+s+"/"
            yr_list = os.listdir(cur)
            for y in yr_list:
                cur_y = cur+y+"/"
                file_list = os.listdir(cur_y)
                for f in file_list:
                    cur_f = cur_y+f
                    data = open(cur_f,"r")
                    json_data = json.load(data)
                    for rec in json_data["data"]["hoverDataList"]:
                        name = rec["name"]
                        count = rec["metric"][0]["count"]
                        amount = rec["metric"][0]["amount"]
                        map_tran_cols["districts"].append(name)
                        map_tran_cols["transaction_count"].append(count)
                        map_tran_cols["transaction_amount"].append(amount)
                        map_tran_cols["states"].append(s)
                        map_tran_cols["years"].append(y)
                        map_tran_cols["quarters"].append(f.strip(".json"))
        df = pd.DataFrame(map_tran_cols)
        return(df)                           

    def get_map_users(self):
        map_user_path = "C:/kannan/code/phonepedata/data/map/user/hover/country/india/state/"
        map_user_list = os.listdir(map_user_path)
        #print(agg_tran_list)

        map_user_cols = {"states":[],"years":[],"quarters":[],"districts":[],"registered_users":[], "app_opens":[]}
        for s in map_user_list:
            cur = map_user_path+s+"/"
            yr_list = os.listdir(cur)

            for y in yr_list:
                cur_y = cur+y+"/"
                file_list = os.listdir(cur_y)
                for f in file_list:
                    cur_f = cur_y+f
                    data = open(cur_f,"r")

                    json_data = json.load(data)
                    try:
                        for rec in json_data["data"]["hoverData"].items():
                            districts = rec[0]
                            registered_users = rec[1]["registeredUsers"]
                            app_opens = rec[1]["appOpens"]
                            map_user_cols["districts"].append(districts)
                            map_user_cols["registered_users"].append(registered_users)
                            map_user_cols["app_opens"].append(app_opens)
                            map_user_cols["states"].append(s)
                            map_user_cols["years"].append(y)
                            map_user_cols["quarters"].append(f.strip(".json"))
                    except:
                        pass 
        df = pd.DataFrame(map_user_cols)
        return(df)                      

    def get_top_trans(self):
        toppath = "C:/kannan/code/phonepedata/data/top/transaction/country/india/state/"
        top_tran_list = os.listdir(toppath)
        #print(agg_tran_list)
        top_tran_cols = {"states":[],"years":[],"quarters":[],"districts":[],"transaction_count":[], "transaction_amount":[]}
        for s in top_tran_list:
            cur = toppath+s+"/"
            yr_list = os.listdir(cur)
            for y in yr_list:
                cur_y = cur+y+"/"
                file_list = os.listdir(cur_y)
                for f in file_list:
                    cur_f = cur_y+f
                    data = open(cur_f,"r")
                    json_data = json.load(data)
                    for rec in json_data["data"]["districts"]:
                        name = rec["entityName"]
                        count = rec["metric"]["count"]
                        amount = rec["metric"]["amount"]
                        top_tran_cols["districts"].append(name)
                        top_tran_cols["transaction_count"].append(count)
                        top_tran_cols["transaction_amount"].append(amount)
                        top_tran_cols["states"].append(s)
                        top_tran_cols["years"].append(y)
                        top_tran_cols["quarters"].append(f.strip(".json"))
        df = pd.DataFrame(top_tran_cols)
        return(df)                          

    def get_top_users(self):
        top_user_path = "C:/kannan/code/phonepedata/data/top/user/country/india/state/"
        top_user_list = os.listdir(top_user_path)
        #print(agg_tran_list)
        top_user_cols = {"states":[],"years":[],"quarters":[],"districts":[],"registered_users":[]}
        for s in top_user_list:
            cur = top_user_path+s+"/"
            yr_list = os.listdir(cur)
            for y in yr_list:
                cur_y = cur+y+"/"
                file_list = os.listdir(cur_y)
                for f in file_list:
                    cur_f = cur_y+f
                    data = open(cur_f,"r")
                    json_data = json.load(data)
                    for rec in json_data["data"]["districts"]:
                        districts = rec["name"]
                        registered_users = rec["registeredUsers"]
                        top_user_cols["districts"].append(districts)
                        top_user_cols["registered_users"].append(registered_users)
                        top_user_cols["states"].append(s)
                        top_user_cols["years"].append(y)
                        top_user_cols["quarters"].append(f.strip(".json"))
        df = pd.DataFrame(top_user_cols)
        return(df)                            