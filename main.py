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


cm = 1/2.54

data = df.groupby('roomid').value_counts()


st.bar_chart(data)




