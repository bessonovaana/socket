import json
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5000,
    database='telephony',
    user="postgres", 
    password="3023"
)

cursor = conn.cursor()

with open("location.json", "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line.strip())

        lat = float(data['latitude'])
        lon = float(data['longitude'])
        timestamp = data['timestamp']
        operator = data.get('network', {}).get('operator', '')
        network_type = data.get('network', {}).get('networkType', 0)
        signal_level = data.get('network', {}).get('signalLevel', 0)
        cell_class = data.get('network', {}).get('cellClass', '')
        network_type_name = data.get('network', {}).get('networkTypeName', '')
        cells_json = data.get('network', {}).get('cells', '')

        if cells_json:
            try:
                cells = json.loads(cells_json) if isinstance(cells_json, str) else cells_json
                if cells and len(cells) > 0:
                    cell = cells[0]
                    identity = cell.get('identity', {})
                    signal = cell.get('signal', {})
                    
                    mcc = identity.get('mcc')
                    mnc = identity.get('mnc')
                    tac = identity.get('tac')
                    pci = identity.get('pci')
                    rsrp = signal.get('rsrp')
            except:
                pass

        cursor.execute("""
            INSERT INTO telephony 
            (Lat, Lon, Alt, Speed, Accuracy, Timestamp, Time, 
             Operator, NetworkType, SignalLevel, CellClass, 
             NetworkTypeName, IsWifi, IsMobile, IsConnected, Cells)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            lat,
            lon,
            data.get('altitude'),
            data.get('speed'),
            data.get('accuracy'),
            timestamp,
            data.get('time'),
            operator,
            network_type,
            signal_level,
            cell_class,
            network_type_name,
            data.get('network', {}).get('isWifi', False),
            data.get('network', {}).get('isMobile', False),
            data.get('network', {}).get('isConnected', False),
            cells_json 
        ))

conn.commit()
cursor.close()
conn.close()
print("Данные добавлены в таблицу telephony")
