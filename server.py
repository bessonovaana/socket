import zmq
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

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5500")
print(" Сервер запущен на порту 5500, ожидание подключений...")

while True:
    try:
        message = socket.recv_string()
        
        try:
            data = json.loads(message)
            print(f" Получены данные: lat={data.get('latitude')}, lon={data.get('longitude')}")
        except json.JSONDecodeError:
            print(f" Ошибка JSON: {message}")
            socket.send_string("OK")
            continue

        lat = float(data['latitude'])
        lon = float(data['longitude'])
        timestamp = data['timestamp']
        operator = data.get('network', {}).get('operator', '')
        network_type = data.get('network', {}).get('networkType', 0)
        signal_level = data.get('network', {}).get('signalLevel', 0)
        rsrp = data.get('network', {}).get('rsrp', 0)
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
                    print(f"RSRP: {signal.get('rsrp')}, PCI: {identity.get('pci')}")
            except:
                pass


        cursor.execute("""
            INSERT INTO telephony 
            (Lat, Lon, Alt, Speed, Accuracy, Timestamp, Time, 
             Operator, NetworkType, SignalLevel, CellClass, 
             NetworkTypeName, IsWifi, IsMobile, IsConnected, Cells, RSRP)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
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
            cells_json,
            rsrp
        ))
        
        conn.commit()  
        
        print(f"Запись добавлена в БД (RSRP={rsrp})")
        socket.send_string("OK")
    except KeyboardInterrupt:
        print("\n Сервер остановлен пользователем")
        break
    except Exception as e:
        print(f" Ошибка: {e}")
        socket.send_string("ERROR")
        conn.rollback() 

cursor.close()
conn.close()
socket.close()
print(" Все соединения закрыты")