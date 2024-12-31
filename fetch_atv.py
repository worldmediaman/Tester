import requests
import os
import json
import time

# URLs für die Anfragen
streaming_url = "https://www.atvavrupa.tv/ajax/streaming"
params_1 = {'menuType': 'CANLIYAYIN'}
video_info_url = "https://videojs.tmgrup.com.tr/getvideo/45d4cd69-814c-4e2e-bdad-11de9e4b9afd/00000000-0000-0000-0000-000000000000"
secure_token_url = "https://securevideotoken.tmgrup.com.tr/webtv/secure"

output_file_path = "result/List/ATV.m3u8"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.atvavrupa.tv/canli-yayin',
    'Origin': 'https://www.atvavrupa.tv',
    'Connection': 'keep-alive'
}

def fetch_and_save_atv():
    try:
        # Senden der ersten Anfrage, um die Streaming-Daten zu erhalten
        response_1 = requests.get(streaming_url, params=params_1, headers=headers)
        response_1.raise_for_status()
        content_1 = response_1.json()
        
        # Debug: Ausgabe der ersten Antwort
        print("Antwortinhalt 1:")
        print(json.dumps(content_1, indent=2))
        
        # Senden der zweiten Anfrage, um die Video-Informationen zu erhalten
        response_2 = requests.get(video_info_url, headers=headers)
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
        response_3 = requests.get(secure_token_url, params=secure_params, headers=headers)
        response_3.raise_for_status()
        content_3 = response_3.json()
        
        # Debug: Ausgabe der dritten Antwort
        print("Antwortinhalt 3:")
        print(json.dumps(content_3, indent=2))
        
        # Extrahieren der dynamischen Parameter aus der dritten Antwort
        session_id = content_3.get('session_id')
        st = content_3.get('st')
        
        # Debug: Überprüfen der extrahierten Werte
        print(f"Extrahierte Werte: session_id={session_id}, st={st}")

        # Überprüfen, ob die Parameter korrekt extrahiert wurden
        if not st or not session_id:
            print("Fehler: st oder session_id konnte nicht extrahiert werden.")
            return
        
        e = str(int(time.time()) + 7200)  # Ablaufzeit in 2 Stunden
        
        # Generieren der vollständigen m3u8-URL
        m3u8_url = f"{base_m3u8_url}?st={st}&e={e}&SessionID={session_id}&StreamGroup=canli-yayin&Site=atvavrupa&DeviceGroup=web"
        
        # Debug: Überprüfen, ob vollständige m3u8-URL korrekt ist
        print("Vollständige m3u8-URL:", m3u8_url)
        
        # Weitere Validierung und Erstellen des M3U8-Inhalts
        if m3u8_url:
            # Sicherstellen, dass der Ausgabeordner existiert
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            
            # Speichern der m3u8-URL in einer Datei mit Zeitstempel
            with open(output_file_path, "w") as f:
                f.write(f"{m3u8_url}\nZeitstempel: {time.ctime()}")
            
            print(f"{output_file_path} Datei erfolgreich erstellt.")
            print("Inhalt:")
            print(m3u8_url)  # Inhalt für Debugging ausgeben
        else:
            print("m3u8-URL in der Antwort nicht gefunden oder nicht gültig.")
    except requests.RequestException as e:
        print(f"Fehler beim Abrufen von ATV: {e}")

if __name__ == "__main__":
    fetch_and_save_atv()
