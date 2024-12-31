import requests
import os
import json

# URL für die POST-Anfrage
post_url = "https://zagent891.h-cdn.com/cmd/get_links_info"
params = {
    'customer': 'atv',
    'zone': 'gen',
    'ver': '1.165.105',
    'url': 'https://www.atvavrupa.tv/canli-yayin'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7',
    'Content-Type': 'text/plain;charset=UTF-8',
    'Origin': 'https://www.atvavrupa.tv',
    'Referer': 'https://www.atvavrupa.tv/',
    'Connection': 'keep-alive'
}

output_file_path = "result/List/ATV.m3u8"

def fetch_and_save_atv():
    try:
        # Senden der POST-Anfrage, um die m3u8-URL zu erhalten
        response = requests.post(post_url, json=params, headers=headers)
        response.raise_for_status()
        content = response.json()
        
        # Debug: Ausgabe der Antwort
        print("Antwortinhalt:")
        print(json.dumps(content, indent=2))
        
        # Extrahieren der m3u8-URL aus der Antwort
        if content.get("error"):
            print("Fehler in der Antwort:", content["error"])
            return

        m3u8_url = content.get("url")
        
        # Weitere Validierung der URL
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
