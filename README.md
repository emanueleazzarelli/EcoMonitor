# EcoMonitor

EcoMonitor è un sistema semplice per il monitoraggio ambientale sviluppato per la classe Quarta ITIS Informatica. Il progetto permette di raccogliere misure di luminosità (luce) e livello di rumore inviate da diversi client, salvarle su un server centrale e visualizzarle attraverso una dashboard interattiva.

## 📁 Struttura del Progetto

- `server.py`: Gestisce le connessioni in ingresso dai client, riceve i dati delle misure e li salva nel file CSV condiviso.
- `client.py`: Legge i dati dai file CSV locali delle misure (luce o rumore), si connette al server via TCP e invia le letture.
- `dashboard.py`: Un'applicazione Streamlit che legge il file CSV centrale e mostra grafici, statistiche e classifiche dei luoghi monitorati.
- `misure.csv`: Il database in formato CSV dove vengono salvati tutti i dati inviati dai vari studenti.
- File `.csv` (es. `Raw Data.csv`, `Amplitudes.csv`): I file contenenti i dati grezzi dei sensori letti dal client.

## 🚀 Come Eseguire il Progetto

### 1. Prerequisiti
Assicurati di avere Python installato sul computer. Per la dashboard, sono necessarie le librerie `streamlit` e `pandas`. Puoi installarle eseguendo:
```bash
pip install streamlit pandas
