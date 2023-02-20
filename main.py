import streamlit as st
import requests
import pandas as pd
import arrow
import json
from datetime import datetime

tab_titles = [
    "Utilisation",
    "Réservations"
]

tabs = st.tabs(tab_titles)

def NumToMonths(shortMonth):
    months = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
    return months[int(shortMonth) - 1]


# with tabs[1]:
#     try :
#         rep = requests.get('https://hpereira.pythonanywhere.com/bookings/')
#         rep.raise_for_status()
#     except requests.exceptions.HTTPError:
#         st.header("⚠️ Impossible de se connecter à l'API. ⚠️")
#         st.write("Vérifiez votre connexion ou contactez le support.")
#     else :     
#         st.title('Réservations :')     
#         data = json.loads(rep.text)
#         df = pd.DataFrame(data)
#         df.drop('id',inplace=True,axis=1)

#         st.write('### Nombre de réservations par salle :')
#         etage = st.selectbox("Sélectionnez l'étage de la salle : ",(1,2,3,4,5,6,7,8,9,'All'))
#         if(etage!='All'):
#             df_filtered = df[df['etage'] == str(etage)]
#         else: 
#             df_filtered = df
#         if(len(df_filtered.index) != 0):
#             st.markdown('- axe x : Id de la salle')
#             st.markdown('- axe y : Nombre de réservations')
#             st.bar_chart(df_filtered['roomid'].value_counts())
#         else:
#             st.warning("Absence de données pour former l'histogramme.")

#         st.write('### Nombre de réservations par jour :')
#         df_filtered1 = df["date"].astype(str).str.split("|", n = 1, expand = True)
#         if(len(df_filtered1.index) != 0):
#             df_filtered1.columns = ["jours", "heures"]
#             st.markdown('- axe x : Date')
#             st.markdown('- axe y : Nombre de réservations')
#             st.bar_chart(df_filtered1["jours"].value_counts())
#         else:
#             st.warning("Absence de données pour former l'histogramme.")

#         st.write('### Nombre de réservations par heure :')
#         df_filtered2 = df["date"].astype(str).str.split("|", n = 1, expand = True)
#         df_filtered2 = df_filtered2[1].astype(str).str.split(":", n = 1, expand = True)
#         if(len(df_filtered2.index) != 0):
#             df_filtered2.columns = ['heures', 'minutes et secondes']
#             st.markdown('- axe x : Heure')
#             st.markdown('- axe y : Nombre de réservations')
#             st.bar_chart(df_filtered2['heures'].value_counts())
#         else:
#             st.warning("Absence de données pour former l'histogramme.")

#         st.write('### Données supplémentaires :')
#         moyenne_jours = int(df_filtered1.groupby('jours').size().mean())
#         moyenne_heures = int(df_filtered2['heures'].mode()[0])
#         col4, col5 = st.columns(2)
#         col6, col7 = st.columns(2)
#         col4.metric("Nombre total de réservations", len(df['roomid']))
#         df_filtered1 = df_filtered1[df_filtered1['jours'] == arrow.now().format('DD-MM-YYYY')]
#         col5.metric("Nombre de réservations aujourd'hui", len(df_filtered1))
#         col6.metric("Nombre moyen de réservations par jour", moyenne_jours)
#         col7.metric("Horaire pendant lequel il y a eu le plus de réservations", str(moyenne_heures) + " Heures")

with tabs[0]:
    try :
        rep = requests.get('https://hpereira.pythonanywhere.com/test/')
        rep.raise_for_status()
    except requests.exceptions.HTTPError:
        st.header("⚠️ Impossible de se connecter à l'API. ⚠️")
        st.write("Vérifiez votre connexion ou contactez le support.")
    else :     
        st.title('Utilisation :')        
        data = json.loads(rep.text)
        df = pd.DataFrame(data)
        indexNames = df[df['etage_kdmap'] == -50].index
        df.drop(indexNames , inplace=True)
        st.markdown("*Une utilisation est comptée comme un retour à la page d'accueil. Cela s'effectue toutes les 45 secondes si la KDMAP a été touchée.*")

        df_filtered3 = df.copy()
        df_filtered3 = df_filtered3["date"].astype(str).str.split("-",expand = True)   
        df_filtered3.columns = ["jours", "mois", "reste"]
        date = datetime.now()
        mois_courant = str(date).split('-')[1]
        df_filtered3 = df_filtered3[df_filtered3['mois'] == mois_courant]
        st.markdown("### Nombre d'utilisation sur le mois de " + NumToMonths(mois_courant) + " :")
        st.markdown("##### " + str(len(df_filtered3)) + " utilisations")

        st.write('### Utilisation globale des KD MAPS :')
        start_color, end_color = st.select_slider(
            'Sélectionnnez le plage temporelle :',
            options=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
            value=('Janvier', 'Décembre')
        )
        mois=['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        index_debut =mois.index(start_color) + 1
        index_fin = mois.index(end_color) + 1
        annee = st.radio(
            "Sélectionnez l'année :",
            ('2023', '2022'),
        )
        df_filtered2 = df.copy()
        df_filtered2[["jours", "mois", "reste"]] = df_filtered2["date"].apply(lambda x: pd.Series(str(x).split("-")))
        df_filtered2[["annee", "reste"]] = df_filtered2["reste"].apply(lambda x: pd.Series(str(x).split("|")))
        df_filtered2 = df_filtered2[(df_filtered2['mois'].astype(int) >= index_debut) & (df_filtered2['mois'].astype(int) <= index_fin) & (df_filtered2['annee'] == annee)]
        if(len(df_filtered2.index) != 0):
            st.markdown('- axe x : Étage de la KD MAP')
            st.markdown("- axe y : Nombre d'utilisations")
            st.bar_chart(df_filtered2['etage_kdmap'].value_counts())
        else:
            st.warning("Absence de données pour former l'histogramme.")

        st.write('### Utilisation détaillée des KD MAPS :')
        etage = st.selectbox("Sélectionnez l'étage de la KD MAP : ", ('All',1,2,3,4,5,6,7,8,9))
        if(etage!='All'):
            df_filtered = df_filtered2[df_filtered2['etage_kdmap'] == str(etage)]
        else: 
            df_filtered = df_filtered2
        if(len(df_filtered.index) != 0):
            df_filtered = df_filtered["date"].astype(str).str.split("|", n = 1, expand = True)
            df_filtered = df_filtered[1].astype(str).str.split(":", n = 1, expand = True)
            df_filtered.columns = ['heures', 'minutes et secondes']
            st.markdown('- axe x : Heure')
            st.markdown("- axe y : Nombre d'utilisations")
            st.bar_chart(df_filtered['heures'].value_counts())
        else:
            st.warning("Absence de données pour former l'histogramme.")

        st.write('### Données supplémentaires :')
        col4, col5 = st.columns(2)
        if(len(df_filtered2.index) != 0):
            df_filtered2 = df_filtered2["date"].astype(str).str.split("|", n = 1, expand = True)
            df_filtered2.columns = ["jours", "heures"]
            moyenne_utilisation = int(df['etage_kdmap'].mode()[0])
            moyenne_nbutilisation = int(df_filtered2.groupby('jours').size().mean())
            col4.metric("KD MAP la plus utilisée", "Étage : " + str(moyenne_utilisation))
            col5.metric("Utilisation journalière moyenne des KD MAPS", moyenne_nbutilisation)
        else:
            st.warning("Absence de données pour former les statistiques.")