import requests
import os
import json

# URLs für die Anfragen
streaming_url = "https://www.atvavrupa.tv/ajax/streaming"
params_1 = {'menuType': 'CANLIYAYIN'}
video_info_url = "https://videojs.tmgrup.com.tr/getvideo/45d4cd69-814c-4e2e-bdad-11de9e4b9afd/00000000-0000-0000-0000-000000000000"
session_url = "https://videojs.tmgrup.com.tr/json/getLiveAdsTimer"

output_file_path = "result/List/ATV.m3u8"

def fetch_and_save_atv():
    try:
        # Senden der ersten Anfrage, um die Streaming-Daten zu erhalten
        response_1 = requests.get(streaming_url, params=params_1)
        response_1.raise_for_status()
        content_1 = response_1.json()
        
        # Debug: Ausgabe der ersten Antwort
        print("Antwortinhalt 1:")
        print(json.dumps(content_1, indent=2))
        
        # Senden der zweiten Anfrage, um die Video-Informationen zu erhalten
        response_2 = requests.get(video_info_url)
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

        # Senden der dritten Anfrage, um die SessionID und andere Parameter zu erhalten
        params_3 = {
            'websiteid': '45d4cd69-814c-4e2e-bdad-11de9e4b9afd',
            'dateminute': '1735609577'
        }
        response_3 = requests.get(session_url, params=params_3)
        response_3.raise_for_status()
        content_3 = response_3.json()
        
        # Debug: Ausgabe der dritten Antwort
        print("Antwortinhalt 3:")
        print(json.dumps(content_3, indent=2))
        
        # Dynamische Parameter hinzufügen
        session_id = "1.2.1151918422.1735605691"
        stream_group = "canli-yayin"
        site = "atvavrupa"
        device_group = "web"
        st = "eW-KN6yUN7ahfDxXDare3g"
        e = "1735655057"
        
        m3u8_url = f"{base_m3u8_url}?st={st}&e={e}&SessionID={session_id}&StreamGroup={stream_group}&Site={site}&DeviceGroup={device_group}"
        
        # Debug: Überprüfen, ob vollständige m3u8-URL korrekt ist
        print("Vollständige m3u8-URL:", m3u8_url)
        
        # Weitere Validierung und Erstellen des M3U8-Inhalts
        if m3u8_url and m3u8_url.endswith('.m3u8'):
            # Erstellen des M3U8-Inhalts
            m3u8_content = f"""#EXTM3U
#EXT-X-VERSION:3

#EXTINF:-1, ATV Avrupa
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
