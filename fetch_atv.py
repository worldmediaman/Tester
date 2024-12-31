import requests
import os
import json

atv_url = "https://www.atvavrupa.tv/canli-yayin"
ajax_url = "https://www.atvavrupa.tv/ajax/streaming"
output_file_path = "result/List/ATV.m3u8"

def fetch_and_save_atv():
    try:
        # Abrufen der Hauptseite
        response = requests.get(atv_url)
        response.raise_for_status()
        
        # Senden einer Ajax-Anfrage, um die Streaming-Daten zu erhalten
        ajax_response = requests.get(ajax_url, params={'menuType': 'CANLIYAYIN'})
        ajax_response.raise_for_status()
        ajax_content = ajax_response.json()
        
        # Debug: Ausgabe der gesamten Ajax-Antwort
        print("Ajax-Antwort:")
        print(json.dumps(ajax_content, indent=2))

        # Extrahieren der m3u8-URL aus der Ajax-Antwort
        m3u8_url = ajax_content.get('data')
        if m3u8_url and m3u8_url.endswith('.m3u8'):
            # Erstellen des M3U8-Inhalts
            m3u8_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3000000,RESOLUTION=1920x1080
{m3u8_url}
"""
            # Sicherstellen, dass der Ausgabeordner existiert
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            
            # Speichern des M3U8-Inhalts in einer Datei
            with open(output_file_path, "w") as f:
                f.write(m3u8_content)
            
            print(f"{output_file_path} Datei erfolgreich erstellt.")
            print("Inhalt:")
            print(m3u8_content)  # Inhalt für Debugging ausgeben
        else:
            print("m3u8-URL im Ajax-Antwortinhalt nicht gefunden oder nicht gültig.")
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen von ATV: {e}")

if __name__ == "__main__":
    fetch_and_save_atv()
