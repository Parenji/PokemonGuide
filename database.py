import time
import pandas as pd
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os

# Percorso del file da monitorare
FILE_TO_WATCH = 'database.xlsx'
SHEET_NAME = 'database'  # nome del foglio da esportare

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if os.path.abspath(event.src_path) == os.path.abspath(FILE_TO_WATCH):
            print(f'Rilevata modifica a {FILE_TO_WATCH}, avvio esportazione del foglio "{SHEET_NAME}"...')
            try:
                # Carica solo il foglio desiderato
                data = pd.read_excel(FILE_TO_WATCH, sheet_name=SHEET_NAME)
                # Esporta in JSON
                json_file = f'{SHEET_NAME}.json'
                data.to_json(json_file, orient='records', force_ascii=False)
                print(f'Salvato {json_file}')
            except Exception as e:
                print(f'Errore durante l\'esportazione: {e}')

if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(FILE_TO_WATCH))
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print(f"In ascolto su modifiche al file {FILE_TO_WATCH}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
