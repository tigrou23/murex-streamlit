import streamlit as st 
import requests
import pandas as pd

st.set_page_config(page_title="Murex analytics", layout="wide")

st.header('Bookings :')

rep = requests.get('http://abdoutlem1997.pythonanywhere.com/bookings/')
jsonResp = rep.text
df = pd.read_json(jsonResp)
df.drop('id',inplace=True,axis=1)
df.groupby('roomid').value_counts().plot.bar()


st.dataframe(df)




