import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Poop Tracker", page_icon="💩")

config = {
    'credentials': {
        'usernames': {
            'Alby': {
                'name': 'Alberto',
                'password': '$2b$12$yJaiHTTk9yYsjUl8Q27Eb.SMrieaQECL.kRSOFuY0ZOaiM3h9b6bC' 
            },
            'Vale': {
                'name': 'Valeria',
                'password': '$2b$12$NqwqFPDYQNfsV4kLIqBXoe1Xu9bkEVlZ/62LNxL.TtpUjpW01s82W'
            },
            'Ale': {
                'name': 'Alessandro',
                'password': '$2b$12$PHyQ8t8HNJwktMYupq.nkeTT22cwiLrNaTZtwHfRCdjVwNsx3PVM2'
            },
            'Jaco': {
                'name': 'Jacopo',
                'password': '$2b$12$dRNHXSi6Au60xDB3doq/OeT5b5UTdShEokn0/6k8la6skvRtT8qwi'
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'una_chiave_segreta_a_caso', # Scrivi lettere a caso qui
        'name': 'cacca_tracker_cookie'
    }
}

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

# Creiamo la finestra di login
name, authentication_status, username = authenticator.login('Login', 'main')

# --- 3. CONTROLLO ACCESSO ---
if authentication_status == False:
    st.error('Username o password non corretti')
elif authentication_status == None:
    st.warning('Inserisci username e password per entrare')

elif authentication_status == True:
    # =======================================================
    #  TUTTA LA TUA APP DEVE STARE QUI DENTRO (INDENTATA)
    # =======================================================
    
    authenticator.logout('Logout', 'sidebar')
    st.sidebar.write(f"Ciao {name}! 👋")
    
    st.title("💩 Poop Tracker - La Sfida")
    
    # Esempio di bottone
    if st.button("Ho fatto la cacca 💩"):
        st.success(f"Bravo {name}! Registrata.")
        # Qui poi metteremo il codice per Google Sheets
    
    st.write("Qui sotto ci saranno i grafici...")