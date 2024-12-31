import logging import http.client as http_client http_client.HTTPConnection.debuglevel = 1 logging.basicConfig() logging.getLogger().setLevel(logging.DEBUG) requests_log = logging.getLogger("requests.packages.urllib3") requests_log.setLevel(logging.DEBUG)

import requests
import json

# URLs für die Anfragen
streaming_url = "https://www.atvavrupa.tv/ajax/streaming"
params_1 = {'menuType': 'CANLIYAYIN'}
video_info_url = "https://videojs.tmgrup.com.tr/getvideo/45d4cd69-814c-4e2e-bdad-11de9e4b9afd/00000000-0000-0000-0000-000000000000"
secure_token_url = "https://securevideotoken.tmgrup.com.tr/webtv/secure"

output_file_path = "result/List/ATV.m3u8"

# Zusätzliche Header und Cookies
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.atvavrupa.tv/canli-yayin',
    'Origin': 'https://www.atvavrupa.tv',
    'Connection': 'keep-alive'
}
cookies = {
    # Füge hier alle relevanten Cookies hinzu
}

def fetch_and_save_atv():
    try:
        # Senden der ersten Anfrage, um die Streaming-Daten zu erhalten
        response_1 = requests.get(streaming_url, params=params_1, headers=headers, cookies=cookies)
        response_1.raise_for_status()
        content_1 = response_1.json()
        
        # Debug: Ausgabe der ersten Antwort
        print("Antwortinhalt 1:")
        print(json.dumps(content_1, indent=2))
        
        # Senden der zweiten Anfrage, um die Video-Informationen zu erhalten
        response_2 = requests.get(video_info_url, headers=headers, cookies=cookies)
        response_2.raise_for_status()
        content_2 = response_2.json()
        
        # Debug: Ausgabe der zweiten Antwort
        print("Antwortinhalt 2:")
        print(json.dumps(content_2, indent=2))
        
        # Extrahieren der Basis-m3u8-URL aus der zweiten Antwort
        video_data = content_2.get("video", {})
        base_m3u8_url = video_data.get("VideoUrl")
        
        # Debug: Überprüfen, ob Basis-m3u8-URL gefunden wurde
        print("Gefundene Basis-m3u8-URL:", base_m3u8_url)

        # Senden der dritten Anfrage, um den Secure Token und andere Parameter zu erhalten
        secure_params = {
            'url': base_m3u8_url,
            'url2': base_m3u8_url
        }
        response_3 = requests.get(secure_token_url, params=secure_params, headers=headers, cookies=cookies)
        response_3.raise_for_status()
        content_3 = response_3.json()
        
        # Debug: Ausgabe der dritten Antwort
        print("Antwortinhalt 3:")
        print(json.dumps(content_3, indent=2))
        
        # Extrahieren der dynamischen Parameter aus der dritten Antwort
        st = content_3.get('Url').split('?st=')[1].split('&')[0]
        session_id = "45d4cd69-814c-4e2e-bdad-11de9e4b9afd"
        
        # Debug: Überprüfen der extrahierten Werte
        print(f"Extrahierte Werte: session_id={session_id}, st={st}")

        # Weiteres Code zum Verarbeiten und Speichern der Daten
        with open(output_file_path, 'w') as file:
            file.write(f"#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=1280000\n{base_m3u8_url}?st={st}&e=1578381600&session_id={session_id}\n")

        print(f"Erfolgreich gespeichert in: {output_file_path}")
    except requests.RequestException as e:
        print(f"Netzwerkfehler: {e}")
    except KeyError as e:
        print(f"Fehlender Schlüssel im Antwortinhalt: {e}")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
    finally:
        print("Fertig mit Aufräumarbeiten.")

# Funktion ausführen
fetch_and_save_atv()
