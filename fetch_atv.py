import os

# Die gefundene m3u8-URL
m3u8_url = "https://trkvz-live.ercdn.net/atvavrupa/atvavrupa_576p.m3u8?st=ne981CQj45Am3u7EetrT1g&e=1735653004&SessionID=1.2.1151918422.1735605691&StreamGroup=canli-yayin&Site=atvavrupa&DeviceGroup=web"
output_file_path = "result/List/ATV.m3u8"

# Sicherstellen, dass der Ausgabeordner existiert
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

# Erstellen des M3U8-Inhalts
m3u8_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=3000000,RESOLUTION=1920x1080
{m3u8_url}
"""

# Speichern des M3U8-Inhalts in einer Datei
with open(output_file_path, "w") as f:
    f.write(m3u8_content)

print(f"{output_file_path} Datei erfolgreich erstellt.")
print("Inhalt:")
print(m3u8_content)  # Inhalt für Debugging ausgeben
