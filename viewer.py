import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import requests

from utils.config import *
from library.mysql_load import *
from library.data_loader import *
from library.wh_loader import *

class PhonepeAnalytics:
    if __name__=="__main__":
        cfg = Configs()
        conf = cfg.get_data_config()
        #print(conf)

        mys = Mysql()
        dl = DataLoader()
        wh = WHLoader()

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response =requests.get(url)
        indian_states = json.loads(response.content)        

        """
        df = dl.get_correct_states()
        op = wh.load_states_to_wh(mys, df)
        print(op)

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
        """

        with st.sidebar:
            selected = option_menu(
            menu_title=None,
            options=["Home","PhonePe Data Analysis","Load Data","Architecture","About"],
            default_index=0
        )

        if selected == "Home":
            st.title(f"PhonePe Data Analytics")  
        if selected == "Architecture":
            st.write("Data product to get data from PhonePe using Python, load into mysql db")
            #image = Image.open('images/arch.drawio.png')
            #st.image(image, caption="Architecture")            
        if selected == "About":
            st.title(f"About")                             
            st.write("This is Kannan Kandasamy")
            st.write("You can reach me at kannanvijay@hotmail.com")
            st.write("Stackoverflow https://stackoverflow.com/users/6466279/kannan-kandasamy")
            st.write("LinkedIn https://www.linkedin.com/in/kannankandasamy/")

        if selected == "PhonePe Data Analysis":
            #st.title(f"You selected {selected}")     

            st.title("PhonePe Data Analysis")
            query = """select question_id, question_name from questions order by question_id ;"""
            qn_df1 = mys.get_data_from_mysql(query)
            question_selected = st.sidebar.selectbox("Select Question", options = qn_df1['question_name'])            

            query = """select distinct years from agg_trans order by years;"""
            yr_df1 = mys.get_data_from_mysql(query)

            query = """select distinct map_state as states from vw_agg_trans order by states;"""
            states_df = mys.get_data_from_mysql(query)     

            query = """select distinct transaction_name from agg_trans order by transaction_name;"""
            trans_df = mys.get_data_from_mysql(query)     

            if question_selected.startswith("1."):
                st.write("Aggregated Transactions by transaction name")

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                state_selected = st.sidebar.multiselect("Select States", options = states_df['states'], default=list(states_df['states'])[0])      
                sts_selected="','".join(i for i in state_selected)                

                query = """select transaction_name, sum(transaction_count) as transaction_count,  round(sum(transaction_amount), 2) as transaction_amount
                                from vw_agg_trans 
                                where years in ('{yr_selected}')
                                and map_state in ('{sts_selected}')
                                group by transaction_name;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,sts_selected=sts_selected))
                #pl_df = mys.get_data_from_mysql(query)
                st.dataframe(pl_df,hide_index=True,use_container_width=True)    

                st.write("In chart")
                #fig1, ax1 = plt.subplots()
                fig1 = px.pie(pl_df, values="transaction_amount", names="transaction_name", title="Transactions by types")
                #ax1.pie(pl_df["transaction_amount"], labels=pl_df["transaction_name"])
                #ax1.axis("equal")
                st.plotly_chart(fig1)

            elif question_selected.startswith("2."):
                st.write("Aggregated Transactions by States")          

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                trans_selected = st.sidebar.multiselect("Select transaction types", options = trans_df['transaction_name'], default=list(trans_df['transaction_name'])[:])      
                tr_selected="','".join(i for i in trans_selected)                       
                 
                query = """select s.map_state as states, sum(a.transaction_count) as transaction_count,  round(sum(a.transaction_amount), 2) as transaction_amount
                                from agg_trans a
                                join states s
                                on a.states=s.existing_state
                                where years in ('{yr_selected}')
                                and transaction_name in ('{trans_selected}')
                                group by s.map_state;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,trans_selected=tr_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True, height=600)                        

                fig = px.choropleth(
                    pl_df,
                    geojson=indian_states,
                    featureidkey='properties.ST_NM',
                    locations='states',
                    color='transaction_count',
                    color_continuous_scale='Blues'
                )
                fig.update_geos(fitbounds="locations", visible=True)

                st.plotly_chart(fig)       
            elif question_selected.startswith("3."):
                st.write("Aggregated Users by Brands")          

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                query = """select brands, sum(transaction_count) as transaction_count,  round(avg(percentage), 2) as percentage
                                from vw_agg_users
                                where years in ('{yr_selected}')
                                group by brands
                                order by transaction_count desc;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True, height=600) 

                fig1 = px.pie(pl_df, values="transaction_count", names="brands", title="Users by Brands")
                st.plotly_chart(fig1)                