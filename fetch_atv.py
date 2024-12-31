import requests
import re
import os

atv_url = "https://www.atvavrupa.tv/canli-yayin"
output_file_path = "result/List/ATV.m3u8"

def fetch_and_save_atv():
    try:
        response = requests.get(atv_url)
        response.raise_for_status()
        content = response.text

        # Suche nach der m3u8-URL im Quellcode der Seite
        match = re.search(r'(https?://[^\s]+\.m3u8)', content)
        if match:
            m3u8_url = match.group(1)

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
            print("m3u8-URL im Seiteninhalt nicht gefunden.")
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen von ATV: {e}")

if __name__ == "__main__":
    fetch_and_save_atv()
