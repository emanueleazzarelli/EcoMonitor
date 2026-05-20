import socket
import csv
import glob
import math

SERVER_ADDRESS = ('127.0.0.1', 12345)

def trova_csv():
    files = glob.glob("*.csv")
    return sorted([f for f in files if f != 'misure.csv'])

def leggi_misure(filepath):
    misure = []
    with open(filepath, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        colonne = reader.fieldnames

        if 'Illuminance (lx)' in colonne:
            col = 'Illuminance (lx)'
            sensore = 'luce'
        elif 'Sound pressure level (dB)' in colonne:
            col = 'Sound pressure level (dB)'
            sensore = 'rumore'
        else:
            return [], None
        for row in reader:
                v = row[col].strip()
                if '∞' in v or v == '':
                    continue
                valore = float(v)
                if math.isfinite(valore):
                    misure.append(round(valore, 2))
    return misure, sensore

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(SERVER_ADDRESS)
        print(f"Connesso al server\n")
    except ConnectionRefusedError:
        print("ERRORE: server non raggiungibile.")
        return

    try:
        studente = input("Il tuo nome: ").strip()
        luogo = input("Luogo: ").strip()

        while True:
            files = trova_csv()
            if not files:
                print("Nessun file CSV trovato.")
                break

            print("\nFile disponibili:")
            for i, f in enumerate(files, 1):
                print(f"  {i}. {f}")

            scelta = input("Scegli file o ESCI: ").strip()
            if scelta.upper() == "ESCI":
                sock.sendall("ESCI".encode())
                break
            if not scelta.isdigit() or not (1 <= int(scelta) <= len(files)):
                print("Scelta non valida.")
                continue

            filepath = files[int(scelta) - 1]
            misure, sensore = leggi_misure(filepath)

            if not misure:
                print("Nessuna misura valida nel file.")
                continue

            print(f"Trovate {len(misure)} misure ({sensore}). Prima: {misure[0]}, Ultima: {misure[-1]}")
            conferma = input(f"Inviare al server? (si/no): ").strip().lower()
            if conferma != 'si':
                continue

            inviate = 0
            for v in misure:
                try:
                    sock.sendall(f"INVIA|{studente}|{sensore}|{v}|{luogo}".encode())
                    risposta = sock.recv(4096).decode()
                    if risposta.startswith("OK"):
                        inviate += 1
                except Exception as e:
                    print(f"Errore: {e}")
                    break

            print(f"Inviate {inviate}/{len(misure)} misure.")

            ancora = input("Vuoi inviare un altro file? (si/no): ").strip().lower()
            if ancora != 'si':
                sock.sendall("ESCI".encode())
                break

    finally:
        sock.close()
        print("Connessione chiusa.")

if __name__ == "__main__":
    main()