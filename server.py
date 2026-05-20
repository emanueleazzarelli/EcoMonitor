import socket
import threading
import queue
import csv
import os
from datetime import datetime

CSV_FILE = 'misure.csv'
coda_misure = queue.Queue()
#inizializzo il file CSV (se non esiste lo crea)
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow(['studente', 'sensore', 'valore', 'luogo', 'data_ora'])
#salva i dati ricavuti nel file
def salva_csv(studente, sensore, valore, luogo, data_ora):
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow([studente, sensore, valore, luogo, data_ora])

def gestione_client(connection, address):
    try:
        print(f"Thread avviato per il client: {address}")
        while True:
            data = connection.recv(4096)
            if not data:
                print(f"Nessun altro dato dal client {address}")
                break

            messaggio = data.decode().strip()
            print(f"Ricevuto dal client {address}: {messaggio}")

            if messaggio.startswith("INVIA"):
                try:
                    parti = messaggio.split("|")
                    studente = parti[1]
                    sensore  = parti[2]
                    valore   = parti[3]
                    luogo    = parti[4]
                    data_ora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    coda_misure.put(messaggio)
                    print(f"Coda: {coda_misure.qsize()} elementi")

                    salva_csv(studente, sensore, valore, luogo, data_ora)
                    print(f"Salvato nel CSV: {studente}, {sensore}, {valore}, {luogo}")

                    coda_misure.get()
                    coda_misure.task_done()

                    risposta = f"OK|{data_ora}"
                except Exception as e:
                    print(f"ERRORE durante INVIA: {e}")
                    risposta = f"ERRORE|{e}"

            elif messaggio == "CODA":
                risposta = f"CODA|{coda_misure.qsize()} misure in attesa"

            elif messaggio == "ESCI":
                connection.sendall("ARRIVEDERCI".encode())
                print(f"Inviato al client {address}: ARRIVEDERCI")
                break

            else:
                risposta = "ERRORE|Comando non riconosciuto. Usa INVIA, CODA o ESCI."

            if messaggio != "ESCI":
                connection.sendall(risposta.encode())
                print(f"Inviato al client {address}: {risposta}")

    except Exception as e:
        print(f"ERRORE GRAVE nel thread {address}: {e}")
    finally:
        connection.close()
        print(f"Connessione chiusa con il client: {address}")

# --- Avvio server ---
init_csv()
server_address = ('127.0.0.1', 12345)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(server_address)
server_socket.listen(5)
print(f"Server in ascolto su {server_address[0]}:{server_address[1]}")

while True:
    connection, client_address = server_socket.accept()
    client_thread = threading.Thread(target=gestione_client, args=(connection, client_address))
    client_thread.start()
