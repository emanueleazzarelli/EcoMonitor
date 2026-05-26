import streamlit as st
import pandas as pd
import os

CSV_FILE = 'misure.csv'
# Titolo e sottotilolo
st.set_page_config(page_title="EcoMonitor Dashboard", layout="wide")
st.title("EcoMonitor Dashboard")
st.caption("Monitoraggio ambientale")

#CSS 
st.markdown("""
<style>
 
    /* Sfondo generale (antracite + teal) */
    .stApp {
        background: linear-gradient(135deg, #1e1e1e, #0f2027);
        color: #e5e7eb;
    }
 
    /* Titolo */
    h1 {
        color: #2dd4bf !important;
        text-shadow: 0px 0px 6px rgba(45,212,191,0.3);
    }
 
    /* Sottotitoli */
    h2, h3 {
        color: #5eead4 !important;
    }
 
    /* Card metriche */
    [data-testid="stMetric"] {
        background-color: rgba(30, 30, 30, 0.8);
        border: 1px solid rgba(45,212,191,0.25);
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    }
   
    [data-testid="stMetricLabel"] {
        color: #a7f3d0 !important;
    }
 
    [data-testid="stMetricValue"] {
        color: #ecfdf5 !important;
        font-family: 'Courier New', monospace;
    }
 
    /* Divider */
    hr {
        border-bottom: 1px solid rgba(45,212,191,0.2);
    }
 
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #121212;
        border-right: 1px solid rgba(45,212,191,0.15);
    }
 
    /* Label (Sensore, Luogo ecc.) */
    label, .stSelectbox label, .stMultiSelect label {
        color: #5eead4 !important;
        font-weight: 600;
    }
 
    /* Select box */
    div[data-baseweb="select"] {
        background-color: #121212 !important;
        color: #e5e7eb !important;
    }
 
    div[data-baseweb="select"] * {
        color: #e5e7eb !important;
    }
 
    /* Tag selezionati */
    span[data-baseweb="tag"] {
        background-color: #14b8a6 !important;
        color: white !important;
        border-radius: 8px !important;
    }
 
</style>
""", unsafe_allow_html=True)

# Controllo se misure.csv esiste
if not os.path.exists(CSV_FILE):
    st.warning("File misure.csv non trovato. Avvia il server e invia alcune misure.")
    st.stop()

df = pd.read_csv(CSV_FILE)

if df.empty:
    st.info("Nessuna misura ancora. Invia dati dal client.")
    st.stop()

df['valore'] = pd.to_numeric(df['valore'], errors='coerce')
df['data_ora'] = pd.to_datetime(df['data_ora'], errors='coerce')
df = df.dropna(subset=['valore'])

# Filtri e menu nella colonna a sinistra
st.sidebar.header("Filtri")
sensori_disponibili = sorted(df['sensore'].unique().tolist())
sensore_sel = st.sidebar.multiselect("Sensore", sensori_disponibili, default=sensori_disponibili)
luoghi_disponibili = sorted(df['luogo'].unique().tolist())
luogo_sel = st.sidebar.multiselect("Luogo", luoghi_disponibili, default=luoghi_disponibili)
studenti_disponibili = sorted(df['studente'].unique().tolist())
studente_sel = st.sidebar.multiselect("Studente", studenti_disponibili, default=studenti_disponibili)
st.sidebar.markdown("---")


df_filt = df[
    df['sensore'].isin(sensore_sel) &
    df['luogo'].isin(luogo_sel) &
    df['studente'].isin(studente_sel)
]

if df_filt.empty:
    st.warning("Nessun dato con i filtri selezionati.")
    st.stop()
 
# KPI
col1, col2, col3, col4 = st.columns(4)
col1.metric("Misure totali", len(df_filt))
col2.metric("Valore medio", f"{df_filt['valore'].mean():.1f}")
col3.metric("Studenti", df_filt['studente'].nunique())
col4.metric("Luoghi", df_filt['luogo'].nunique())

st.divider()


# Valore medio per luogo
st.subheader("Valore medio per luogo (per sensore)")
for sensore in sensore_sel:
    df_s = df_filt[df_filt['sensore'] == sensore]
    if not df_s.empty:
        st.markdown(f"**{sensore.capitalize()}**")
        media_luogo = df_s.groupby('luogo')['valore'].mean().sort_values(ascending=False)
        st.bar_chart(media_luogo)

st.divider()

# Classifica dei luoghi
st.subheader("Classifica luoghi (valore medio)")
classifica = df_filt.groupby(['luogo', 'sensore'])['valore'].mean().reset_index()
classifica.columns = ['Luogo', 'Sensore', 'Valore medio']
classifica = classifica.sort_values('Valore medio', ascending=False).reset_index(drop=True)
classifica.index += 1
st.dataframe(classifica, use_container_width=True)

st.divider()

# Misure per studente
st.subheader("Numero di misure per studente")
st.bar_chart(df_filt['studente'].value_counts())

st.divider()

# Statistiche per sensore
st.subheader("Statistiche per sensore")
stats = df_filt.groupby('sensore')['valore'].agg(['count', 'mean', 'min', 'max']).reset_index()
stats.columns = ['Sensore', 'Misure', 'Media', 'Min', 'Max']
stats['Media'] = stats['Media'].round(1)
stats['Min'] = stats['Min'].round(1)
stats['Max'] = stats['Max'].round(1)
st.dataframe(stats, use_container_width=True)

st.divider()

st.subheader("Tabella completa dei dati")
st.dataframe(df_filt.sort_values('data_ora', ascending=False), use_container_width=True)

st.caption("Aggiorna la pagina per vedere i nuovi dati.")
