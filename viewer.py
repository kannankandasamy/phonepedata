import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import requests
from PIL import Image

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

        df = dl.get_population_by_states()
        op = wh.load_states_population_to_wh(mys, df)
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
            st.write("Data Sources - Population")
            st.write("https://statisticstimes.com/demographics/india/indian-states-population.php")
            image = Image.open('images/phonepe_arch.drawio.png')
            st.image(image, caption="Architecture")            
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
            question_selected = st.sidebar.selectbox("Select Analysis", options = qn_df1['question_name'])            

            query = """select distinct years from agg_trans order by years;"""
            yr_df1 = mys.get_data_from_mysql(query)

            query = """select distinct map_state as states from vw_agg_trans order by states;"""
            states_df = mys.get_data_from_mysql(query)     

            query = """select distinct transaction_name from agg_trans order by transaction_name;"""
            trans_df = mys.get_data_from_mysql(query)     

            if question_selected.startswith("1."):
                st.write("Transactions by transaction name")

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                state_selected = st.sidebar.multiselect("Select States", options = states_df['states'], default=list(states_df['states'])[0])      
                sts_selected="','".join(i for i in state_selected)                

                query = """select transaction_name, sum(transaction_count) as transaction_count,  round(sum(transaction_amount), 2) as transaction_amount
                                from vw_agg_trans 
                                where years in ('{yr_selected}')
                                and map_state in ('{sts_selected}')
                                group by transaction_name
                                order by transaction_count desc;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,sts_selected=sts_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)    

                #fig1 = px.pie(pl_df, values="transaction_count", names="transaction_name", title="Transactions by types")
                #st.plotly_chart(fig1)
                fig = go.Figure(go.Bar(x=pl_df["transaction_name"],y=pl_df["transaction_count"],marker_color=pl_df["transaction_count"]))
                fig.update_layout(
                    updatemenus=[
                        dict(direction="down", type="buttons",font={"color":"blue"},
                            buttons=([
                                dict(args=["type","bar"], label="bar view", method="restyle"),        
                                dict(args=["type","pie"], label="pie view", method="restyle"),
                                dict(args=["type","scatter"], label="scatter view", method="restyle"),
                            ]))
                    ]
                )                            
                st.plotly_chart(fig)

            elif question_selected.startswith("2."):
                st.write("Aggregated Transactions by States")          

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                trans_selected = st.sidebar.multiselect("Select transaction types", options = trans_df['transaction_name'], default=list(trans_df['transaction_name'])[:])      
                tr_selected="','".join(i for i in trans_selected)       

                op_selected = st.sidebar.selectbox("Report type", options = ['Transaction Count','Transaction Amount'])
                if op_selected=='Transaction Count':
                    option_details = 'transaction_count'
                else:
                    option_details = 'transaction_amount'                                
                 
                query = """select map_state as states, sum(transaction_count) as transaction_count,  round(sum(transaction_amount), 2) as transaction_amount
                                from vw_agg_trans
                                where years in ('{yr_selected}')
                                and transaction_name in ('{trans_selected}')
                                group by map_state;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,trans_selected=tr_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True, height=400)                        

                fig = px.choropleth(
                    pl_df,
                    geojson=indian_states,
                    featureidkey='properties.ST_NM',
                    locations='states',
                    color=option_details,
                    color_continuous_scale='speed'
                )
                fig.update_geos(fitbounds="locations", visible=True)

                st.plotly_chart(fig)       
            elif question_selected.startswith("3."):
                st.write("Usage Percentge by Brands")          

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                query = """select brands, sum(transaction_count) as transaction_count,  round(avg(percentage), 2) as percentage
                                from vw_agg_users
                                where years in ('{yr_selected}')
                                group by brands
                                order by transaction_count desc;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True, height=400) 

                fig1 = px.pie(pl_df, values="transaction_count", names="brands", title="Users by Brands")
                st.plotly_chart(fig1)       

            elif question_selected.startswith("4."):
                st.write("Transactions by districts")          

                state_selected = st.sidebar.selectbox("Select States", options = states_df['states'])      
                #sts_selected="','".join(i for i in state_selected)  

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)                

                query = """select districts, sum(transaction_count) as transaction_count,  round(sum(transaction_amount), 2) as transaction_amount
                                from vw_map_trans
                                where map_state in ('{state_selected}')
                                and years in ('{yr_selected}')
                                group by districts
                                order by districts;"""
                pl_df = mys.get_data_from_mysql(query.format(state_selected=state_selected,yr_selected=yr_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)     

                fig = px.bar(pl_df, x="districts", y="transaction_count", color="districts", title="In chart", labels={"transaction_count":"Transaction counts"})
                st.plotly_chart(fig)

            elif question_selected.startswith("5."):
                st.write("Registered Users by districts")          

                state_selected = st.sidebar.selectbox("Select States", options = states_df['states'])      
                #sts_selected="','".join(i for i in state_selected)  

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)                

                query = """select districts, sum(registered_users) as registered_users,  sum(app_opens) as app_opens
                                from vw_map_users
                                where map_state in ('{state_selected}')
                                and years in ('{yr_selected}')
                                group by districts
                                order by districts;"""
                pl_df = mys.get_data_from_mysql(query.format(state_selected=state_selected,yr_selected=yr_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)     

                #fig = px.bar(pl_df, x="districts", y="registered_users", color="districts", title="In chart")

                fig = go.Figure(go.Bar(x=pl_df["districts"],y=pl_df["registered_users"],marker_color=pl_df["registered_users"]))
                fig.update_layout(
                    updatemenus=[
                        dict(direction="down", type="buttons",font={"color":"blue"},
                            buttons=([
                                dict(args=["type","bar"], label="bar view", method="restyle"),        
                                dict(args=["type","pie"], label="pie view", method="restyle"),
                                dict(args=["type","scatter"], label="scatter view", method="restyle"),
                            ]))
                    ]
                )                    
                st.plotly_chart(fig)

            elif question_selected.startswith("6."):
                st.write("Transactions and Users by districts")          

                state_selected = st.sidebar.selectbox("Select States", options = states_df['states'])      
                #sts_selected="','".join(i for i in state_selected)  

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)                

                query = """select mu.districts, sum(mu.registered_users) as registered_users,  sum(mu.app_opens) as app_opens
                                    , sum(mt.transaction_count) as transaction_count, sum(mt.transaction_amount) as transaction_amount
                                from vw_map_users mu
                                join vw_map_trans mt
                                on mu.states = mt.states
                                and mu.years = mt.years
                                and mu.quarters = mt.quarters
                                and mu.districts = mt.districts
                                where mu.map_state in ('{state_selected}')
                                and mu.years in ('{yr_selected}')
                                group by mu.districts
                                order by mu.districts;"""
                pl_df = mys.get_data_from_mysql(query.format(state_selected=state_selected,yr_selected=yr_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)    

                fig = px.bar(pl_df, x="districts", y=["app_opens", "transaction_count"], title="Users and Transactions")
                st.plotly_chart(fig)

            elif question_selected.startswith("7."):
                st.write("Aggregated Transactions by Years")          

                state_selected = st.sidebar.selectbox("Select States", options = states_df['states'])      
                #sts_selected="','".join(i for i in state_selected)  

                query = """with cte as (
                                select map_state, years, transaction_name, sum(transaction_count) as transaction_count from vw_agg_trans
                                where map_state in ('{state_selected}')
                                group by map_state, years, transaction_name
                            )
                            select 
                                transaction_name,
                                sum(case years when '2018' then transaction_count end) as '2018',
                                sum(case years when '2019' then transaction_count end) as '2019', 
                                sum(case years when '2020' then transaction_count end) as '2020',
                                sum(case years when '2021' then transaction_count end) as '2021',
                                sum(case years when '2022' then transaction_count end) as '2022',
                                sum(case years when '2023' then transaction_count end) as '2023'
                            from cte
                            group by 
                                transaction_name"""
                pl_df = mys.get_data_from_mysql(query.format(state_selected=state_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)    

                query = """select map_state, years, transaction_name, sum(transaction_count) as transaction_count from vw_agg_trans
                            where map_state in ('{state_selected}')
                            group by map_state, years, transaction_name""" 
                df1 = mys.get_data_from_mysql(query.format(state_selected=state_selected))
                fig = px.line(df1, x="years", y="transaction_count", color="transaction_name",markers=True)
                st.plotly_chart(fig)           

            elif question_selected.startswith("8."):
                st.write("Registered Users by Years")          

                state_selected = st.sidebar.selectbox("Select States", options = states_df['states'])      
                #sts_selected="','".join(i for i in state_selected)  

                query = """with cte as (
                                select map_state, years, districts, sum(registered_users) as registered_users from vw_top_users
                                where map_state in ('{state_selected}')
                                group by map_state, years, districts
                            )
                            select 
                                districts,
                                coalesce(sum(case years when '2018' then registered_users end),0) as '2018',
                                coalesce(sum(case years when '2019' then registered_users end),0) as '2019', 
                                coalesce(sum(case years when '2020' then registered_users end),0) as '2020',
                                coalesce(sum(case years when '2021' then registered_users end),0) as '2021',
                                coalesce(sum(case years when '2022' then registered_users end),0) as '2022',
                                coalesce(sum(case years when '2023' then registered_users end),0) as '2023'
                            from cte
                            group by 
                                districts;"""
                pl_df = mys.get_data_from_mysql(query.format(state_selected=state_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)    

                query = """select map_state, years, districts, sum(registered_users) as registered_users from vw_top_users
                            where map_state in ('{state_selected}')
                            group by map_state, years, districts""" 
                df1 = mys.get_data_from_mysql(query.format(state_selected=state_selected))
                fig = px.line(df1, x="years", y="registered_users", color="districts",markers=True)
                st.plotly_chart(fig)                                

            elif question_selected.startswith("9."):
                st.write("Transactions by Years on brands")          

                state_selected = st.sidebar.selectbox("Select States", options = states_df['states'])      
                #sts_selected="','".join(i for i in state_selected)  

                query = """with cte as (
                                select map_state, years, brands, sum(transaction_count) as transaction_count from vw_agg_users
                                where map_state in ('{state_selected}')
                                group by map_state, years, brands
                            )
                            select 
                                brands,
                                sum(case years when '2018' then transaction_count end) as '2018',
                                sum(case years when '2019' then transaction_count end) as '2019', 
                                sum(case years when '2020' then transaction_count end) as '2020',
                                sum(case years when '2021' then transaction_count end) as '2021',
                                sum(case years when '2022' then transaction_count end) as '2022',
                                sum(case years when '2023' then transaction_count end) as '2023'
                            from cte
                            group by 
                                brands;"""
                pl_df = mys.get_data_from_mysql(query.format(state_selected=state_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)    

                query = """select map_state, years, brands, sum(transaction_count) as transaction_count from vw_agg_users
                            where map_state in ('{state_selected}')
                            group by map_state, years, brands""" 
                df1 = mys.get_data_from_mysql(query.format(state_selected=state_selected))
                fig = px.line(df1, x="years", y="transaction_count", color="brands",markers=True)
                st.plotly_chart(fig)           
            elif question_selected.startswith("10."):
                st.write("Users by States")          

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                op_selected = st.sidebar.selectbox("Report type", options = ['Registered Users','Application Usage'])
                if op_selected=='Registered Users':
                    option_details = 'registered_users'
                else:
                    option_details = 'app_opens'
                 
                query = """select map_state as states, sum({option_details}) as '{op_selected}'
                                from vw_map_users
                                where years in ('{yr_selected}')
                                group by map_state
                                order by map_state;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected, option_details=option_details, op_selected=op_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True, height=400)                        

                #st.write("Registered users In map")
                fig = px.choropleth(
                    pl_df,
                    geojson=indian_states,
                    featureidkey='properties.ST_NM',
                    locations='states',
                    color=op_selected,
                    color_continuous_scale='Oranges'
                )
                fig.update_geos(fitbounds="locations", visible=True)

                st.plotly_chart(fig)  

            elif question_selected.startswith("11."):
                st.write("Per Capita Users by States")          

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                op_selected = st.sidebar.selectbox("Report type", options = ['Registered Users','Application Usage'])
                if op_selected=='Registered Users':
                    option_details = 'registered_users'
                else:
                    option_details = 'app_opens'
                 
                query = """select map_state as states, sum({option_details}/population) as '{op_selected}'
                                from vw_map_users
                                where years in ('{yr_selected}')
                                group by map_state
                                order by map_state;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected, option_details=option_details, op_selected=op_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True, height=400)                        

                fig = px.choropleth(
                    pl_df,
                    geojson=indian_states,
                    featureidkey='properties.ST_NM',
                    locations='states',
                    color=op_selected,
                    color_continuous_scale='sunsetdark'
                )
                fig.update_geos(fitbounds="locations", visible=True)

                st.plotly_chart(fig)                  
            elif question_selected.startswith("12."):
                st.write("PerCapita Transactions by States")          

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                trans_selected = st.sidebar.multiselect("Select transaction types", options = trans_df['transaction_name'], default=list(trans_df['transaction_name'])[:])      
                tr_selected="','".join(i for i in trans_selected)       

                op_selected = st.sidebar.selectbox("Report type", options = ['Transaction Count','Transaction Amount'])
                if op_selected=='Transaction Count':
                    option_details = 'transaction_count'
                else:
                    option_details = 'transaction_amount'                                
                 
                query = """select map_state as states, sum(transaction_count/population) as transaction_count,  round(sum(transaction_amount/population), 2) as transaction_amount
                                from vw_agg_trans
                                where years in ('{yr_selected}')
                                and transaction_name in ('{trans_selected}')
                                group by map_state;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,trans_selected=tr_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True, height=400)                        

                fig = px.choropleth(
                    pl_df,
                    geojson=indian_states,
                    featureidkey='properties.ST_NM',
                    locations='states',
                    color=option_details,
                    color_continuous_scale='Reds'
                )
                fig.update_geos(fitbounds="locations", visible=True)

                st.plotly_chart(fig)                      
            elif question_selected.startswith("13."):
                st.write("Transactions - states comparison")

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                state_selected = st.sidebar.multiselect("Select States", options = states_df['states'], default=list(states_df['states'])[0])      
                sts_selected="','".join(i for i in state_selected)                

                query = """select transaction_name, sum(transaction_count) as transaction_count,  round(sum(transaction_amount), 2) as transaction_amount
                                from vw_agg_trans 
                                where years in ('{yr_selected}')
                                and map_state in ('{sts_selected}')
                                group by transaction_name
                                order by transaction_name;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,sts_selected=sts_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)    

                query = """select map_state, transaction_name, sum(transaction_count) as transaction_count,  round(sum(transaction_amount), 2) as transaction_amount
                                from vw_agg_trans 
                                where years in ('{yr_selected}')
                                and map_state in ('{sts_selected}')
                                group by map_state,transaction_name
                                order by map_state,transaction_name;"""
                pl_df2 = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,sts_selected=sts_selected))                

                fig1 = px.line(pl_df2, x="transaction_name", y="transaction_count", title="Transactions by types", color="map_state")
                st.plotly_chart(fig1)
                #fig = go.Figure(go.Bar(x=pl_df2["transaction_name"],y=pl_df2["transaction_count"],marker_color=pl_df2["transaction_count"]))
                #fig.update_layout(
                #    updatemenus=[
                #        dict(direction="down", type="buttons",font={"color":"blue"},
                #            buttons=([
                #                dict(args=["type","bar"], label="bar view", method="restyle"),        
                #                dict(args=["type","pie"], label="pie view", method="restyle"),
                #                dict(args=["type","scatter"], label="scatter view", method="restyle"),
                #            ]))
                #    ]
                #)                            
                #st.plotly_chart(fig)        
                # 
            elif question_selected.startswith("14."):
                st.write("PerCapita Transactions - states comparison by Amount")

                year_selected = st.sidebar.multiselect("Select Year", options = yr_df1['years'], default=list(yr_df1['years'])[:])      
                yr_selected="','".join(i for i in year_selected)

                state_selected = st.sidebar.multiselect("Select States", options = states_df['states'], default=list(states_df['states'])[0])      
                sts_selected="','".join(i for i in state_selected)                

                query = """select transaction_name, sum(transaction_count/population) as transaction_count,  round(sum(transaction_amount/population), 2) as transaction_amount
                                from vw_agg_trans 
                                where years in ('{yr_selected}')
                                and map_state in ('{sts_selected}')
                                group by transaction_name
                                order by transaction_name;"""
                pl_df = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,sts_selected=sts_selected))
                st.dataframe(pl_df,hide_index=True,use_container_width=True)    

                query = """select map_state, transaction_name, sum(transaction_count/population) as transaction_count,  round(sum(transaction_amount/population), 2) as transaction_amount
                                from vw_agg_trans 
                                where years in ('{yr_selected}')
                                and map_state in ('{sts_selected}')
                                group by map_state,transaction_name
                                order by map_state,transaction_name;"""
                pl_df2 = mys.get_data_from_mysql(query.format(yr_selected=yr_selected,sts_selected=sts_selected))                

                fig1 = px.line(pl_df2, x="transaction_name", y="transaction_amount", title="Transactions Amounts", color="map_state")
                st.plotly_chart(fig1)                        

                fig2 = px.line(pl_df2, x="transaction_name", y="transaction_count", title="Transactions Counts", color="map_state")
                st.plotly_chart(fig2)   
