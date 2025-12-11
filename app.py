import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection # <--- Nuova libreria!

# --- 1. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Poop Tracker", page_icon="💩")

# --- 2. CONFIGURAZIONE UTENTI ---
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

# --- 3. GESTIONE LOGIN ---
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

authenticator.login(location='main')

# --- 4. LOGICA DELL'APP ---
if st.session_state["authentication_status"]:
    
    # Recuperiamo i dati utente
    name = st.session_state["name"]
    authenticator.logout(location='sidebar')
    st.sidebar.title(f"Ciao {name} 👋")
    
    st.title("💩 Poop Tracker - La Sfida")

    # --- CONNESSIONE GOOGLE SHEETS ---
    # Crea la connessione usando i dati che hai messo in secrets.toml
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Funzione per leggere dal foglio online
    # --- CONNESSIONE GOOGLE SHEETS ---
    conn = st.connection("gsheets", type=GSheetsConnection)

    URL_SHEET = "https://docs.google.com/spreadsheets/d/1SXonAZi5E_ixhZBhezKzUHk5EUqSBGchZ4nfDpxcGgo/edit?pli=1&gid=0#gid=0" 

    def carica_dati():
        try:
            # Passiamo il link esplicitamente (spreadsheet=URL_SHEET)
            return conn.read(spreadsheet=URL_SHEET, worksheet="Foglio1", usecols=[0, 1, 2, 3], ttl=0)
        except Exception as e:
            # Se vuoi vedere l'errore nel terminale in caso di problemi:
            # print(e) 
            return pd.DataFrame(columns=['Utente', 'Data', 'Orario', 'Note'])

    def salva_cacca(utente, note):
        df_esistente = carica_dati()
        
        adesso = datetime.now()
        nuova_riga = pd.DataFrame({
            'Utente': [utente],
            'Data': [adesso.strftime("%Y-%m-%d")],
            'Orario': [adesso.strftime("%H:%M")],
            'Note': [note]
        })
        
        df_aggiornato = pd.concat([df_esistente, nuova_riga], ignore_index=True)
        
        # Anche qui passiamo il link esplicitamente
        conn.update(spreadsheet=URL_SHEET, worksheet="Foglio1", data=df_aggiornato)
    # --- INTERFACCIA ---
    st.subheader("Nuova registrazione")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        note_input = st.text_input("Note (opzionale)", placeholder="Es. Epica...")
    
    with col2:
        st.write("") 
        st.write("") 
        # Callback per salvare
        if st.button("AGGIUNGI 💩", type="primary"):
            with st.spinner('Sto inviando al cloud...'):
                salva_cacca(name, note_input)
            st.success("Salvata nel cloud! ☁️")
            st.balloons()
            # Ricarica la pagina per mostrare i dati aggiornati
            st.rerun()

    # --- CLASSIFICA E STORICO ---
    st.divider()
    
    # Carichiamo i dati freschi da Google
    df = carica_dati()
    
    # Assicuriamoci che non ci siano righe vuote strane
    df = df.dropna(subset=['Utente'])

    if not df.empty:
        st.subheader("🏆 Classifica Re del Trono")
        # Conta le occorrenze
        classifica = df['Utente'].value_counts()
        st.bar_chart(classifica)

        st.subheader("📜 Storico Movimenti")
        # Mostra le ultime 10 (tail) invertite (così la più recente è in alto)
        st.dataframe(df.tail(10).iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("Nessun dato nel Cloud. Inaugura tu il foglio!")

# --- GESTIONE ERRORI LOGIN ---
elif st.session_state["authentication_status"] is False:
    st.error('Username o password non corretti')
elif st.session_state["authentication_status"] is None:
    st.warning('Inserisci le credenziali')