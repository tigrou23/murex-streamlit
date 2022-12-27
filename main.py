import streamlit as st
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import arrow

def reservations():

    try :
        rep = requests.get('https://hpereira.pythonanywhere.com/bookings/')
        rep.raise_for_status()
    except requests.exceptions.HTTPError:
        st.header("⚠️ Impossible de se connecter à l'API. ⚠️")
        st.write("Vérifiez votre connexion ou contactez le support.")
    else :     
        st.title('Réservations :')
        st.write('### Nombre de réservations par salle :')

        jsonResp = rep.text
        df = pd.read_json(jsonResp)
        df.drop('id',inplace=True,axis=1)

        etage = st.selectbox("Sélectionnez l'étage de la salle : ",(1,2,3,4,5,6,7,8,9,'All'))
        if(etage!='All'):
            df_filtered = df[df['etage'] == etage]
        else: 
            df_filtered = df
        st.bar_chart(df_filtered['roomid'].value_counts())


        st.write('### Nombre de réservations par jour :')
        df_filtered1 = df["date"].astype(str).str.split(" ", n = 1, expand = True)
        df_filtered1.columns = ["jours", "heures"]
        st.bar_chart(df_filtered1["jours"].value_counts())

        st.write('### Nombre de réservations par heure :')
        df_filtered2 = df["date"].astype(str).str.split(" ", n = 1, expand = True)
        df_filtered2 = df_filtered2[1].astype(str).str.split(":", n = 1, expand = True)
        df_filtered2.columns = ['heures', 'minutes et secondes']
        st.bar_chart(df_filtered2['heures'].value_counts())

        st.write('### Données supplémentaires :')
        moyenne_jours = float(df_filtered1.groupby('jours').size().mean())
        moyenne_heures = int(df_filtered2['heures'].mode())
        col4, col5 = st.columns(2)
        col6, col7 = st.columns(2)
        col4.metric("Nombre total de réservations", len(df['roomid']))
        df_filtered1 = df_filtered1[df_filtered1['jours'] == arrow.now().format('YYYY-MM-DD')]
        col5.metric("Nombre de réservations aujourd'hui", len(df_filtered1))
        col6.metric("Nombre moyen de réservations par jour", moyenne_jours)
        col7.metric("Horaire pendant lequel l'utilisation est la plus élevée", str(moyenne_heures) + " Heures")

page_names_to_funcs = {
    "Réservations": reservations,

}

demo_name = st.sidebar.selectbox("Choix de la thématique :", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()