import streamlit as st 
import requests
import pandas as pd

st.set_page_config(page_title="Murex analytics", layout="wide")

st.header('Bookings :')

rep = requests.get('http://abdoutlem1997.pythonanywhere.com/bookings/')
jsonResp = rep.text
df = pd.read_json(jsonResp)


st.dataframe(df)




