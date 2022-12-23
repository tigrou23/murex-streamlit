import streamlit as st 
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Murex analytics", layout="wide")

st.header('Bookings :')

rep = requests.get('http://abdoutlem1997.pythonanywhere.com/bookings/')
jsonResp = rep.text


df = pd.read_json(jsonResp)
df.drop('id',inplace=True,axis=1)




etage = st.selectbox('Etage',(1,2,3,4,5,6,'All'))


if(etage!='All'):
    df_filtered = df[df['etage']== etage]
else: 
    df_filtered = df



st.bar_chart(df_filtered['roomid'].value_counts())










