# EcoMonitor

EcoMonitor è un sistema semplice per il monitoraggio ambientale sviluppato per la classe Quarta ITIS Informatica. Il progetto permette di raccogliere misure di luminosità (luce) e livello di rumore inviate da diversi client, salvarle su un server centrale e visualizzarle attraverso una dashboard interattiva.

## 📁 Struttura del Progetto

- server.py: Gestisce le connessioni in ingresso dai client, riceve i dati delle misure e li salva nel file CSV condiviso.
- client.py: Legge i dati dai file CSV locali delle misure (luce o rumore), si connette al server via TCP e invia le letture.
- dashboard.py: Un'applicazione Streamlit che legge il file CSV centrale e mostra grafici, statistiche e classifiche dei luoghi monitorati.
- misure.csv: Il database in formato CSV dove vengono salvati tutti i dati inviati dai vari studenti.
- File ".csv" (es. "Raw Data.csv", "Amplitudes.csv"): I file contenenti i dati dei sensori letti dal client.

## 🚀 Come Eseguire il Progetto

### 1. Prerequisiti
Assicurati di avere Python installato sul computer. Per la dashboard, sono necessarie le librerie streamlit e pandas. Puoi installarle eseguendo:
"pip install streamlit pandas"

### 2. Avvio del Server
Esegui per primo il server centrale. Rimarrà in ascolto sulla porta standard 12345 per ricevere i dati:
"python server.py"

### 3. Avvio del Client 
Apri un secondo terminale ed esegui il client per selezionare e trasmettere i dati dei tuoi sensori al server:
"python client.py"

### 4. Avvio della Dashboard
Per visualizzare l'interfaccia web con i grafici e le statistiche in tempo reale, esegui:
"python -m streamlit run dashboard.py"
