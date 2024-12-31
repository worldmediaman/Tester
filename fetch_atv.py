import requests
import re
import os

loader_url = "https://player.h-cdn.com/loader.js?customer=atv"
output_file_path = "result/List/ATV.m3u8"

def fetch_and_save_atv():
    try:
        # Laden des loader.js Skripts
        response = requests.get(loader_url)
        response.raise_for_status()
        content = response.text
        
        # Debug: Ausgabe des gesamten Skriptinhalts
        print("Skriptinhalt:")
        print(content[:1000])  # Ausgabe der ersten 1000 Zeichen zur Überprüfung
        
        # Suchen nach der m3u8-URL im Skript
        m3u8_url = re.search(r'(https?://[^\s]+\.m3u8[^\s]*)', content)
        if m3u8_url:
            m3u8_url = m3u8_url.group(1)

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
            print("m3u8-URL im Skriptinhalt nicht gefunden oder nicht gültig.")
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen von ATV: {e}")

if __name__ == "__main__":
    fetch_and_save_atv()
