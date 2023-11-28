import streamlit as st
import plotly.express as px
import requests
import json

data = {}

data['info'] = ['San Francisco', 'Los Angeles', 'New York']
 
url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response =requests.get(url)
data1 = json.loads(response.content)     
print(data1)   

