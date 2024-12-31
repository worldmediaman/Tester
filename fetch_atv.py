import requests
import re
import os

loader_url = "https://player.h-cdn.com/loader.js?customer=atv"
config_url = "https://player.h-cdn.com/config.js?customer=atv"
output_file_path = "result/List/ATV.m3u8"

def fetch_and_save_atv():
    try:
        # Laden des loader.js Skripts
        response = requests.get(loader_url)
        response.raise_for_status()
        loader_content = response.text

        # Laden des config.js Skripts
        response = requests.get(config_url)
        response.raise_for_status()
        config_content = response.text

        # Debug: Ausgabe der ersten 1000 Zeichen der Skriptinhalte zur Überprüfung
        print("Loader Skriptinhalt:")
        print(loader_content[:1000])
        print("Config Skriptinhalt:")
        print(config_content[:1000])
        
        # Suchen nach der m3u8-URL im config.js Skript
        m3u8_url = re.search(r'(https?://[^\s]+\.m3u8[^\s]*)', config_content)
        if not m3u8_url:
            # Falls keine URL im config.js Skript gefunden wurde, im loader.js Skript suchen
            m3u8_url = re.search(r'(https?://[^\s]+\.m3u8[^\s]*)', loader_content)
        
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
            print("m3u8-URL in den Skriptinhalten nicht gefunden oder nicht gültig.")
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen von ATV: {e}")

if __name__ == "__main__":
    fetch_and_save_atv()
