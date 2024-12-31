import requests
import os
import json

request_url = "https://zagent891.h-cdn.com/cmd/get_links_info"
params = {
    'customer': 'atv',
    'zone': 'gen',
    'ver': '1.165.105',
    'url': 'https://www.atvavrupa.tv/canli-yayin'
}
output_file_path = "result/List/ATV.m3u8"

def fetch_and_save_atv():
    try:
        # Senden einer Anfrage, um die Streaming-Daten zu erhalten
        response = requests.get(request_url, params=params)
        response.raise_for_status()
        content = response.json()
        
        # Debug: Ausgabe der gesamten Antwort
        print("Antwortinhalt:")
        print(json.dumps(content, indent=2))

        # Extrahieren der m3u8-URL aus der Antwort
        m3u8_url = None
        # Wir gehen davon aus, dass die URL im Wert von 'data' oder 'url' liegt.
        if 'data' in content:
            m3u8_url = content['data']
        elif 'url' in content:
            m3u8_url = content['url']
        
        # Weitere Validierung der URL
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
            print("m3u8-URL in der Antwort nicht gefunden oder nicht gültig.")
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen von ATV: {e}")

if __name__ == "__main__":
    fetch_and_save_atv()
