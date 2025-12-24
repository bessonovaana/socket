import matplotlib.pyplot as plt
import psycopg2
import numpy as np


conn = psycopg2.connect(
    host="localhost",
    port=5000,
    database='telephony',
    user="postgres", 
    password="3023"   
)
cursor = conn.cursor()

cursor.execute("""
    SELECT Lat, Lon, SignalLevel, Cells 
    FROM telephony 
    ORDER BY Id DESC LIMIT 2000
""")
results = cursor.fetchall()

lats = [float(row[0]) for row in results]
lons = [float(row[1]) for row in results]

signal_levels = [int(row[2]) if row[2] is not None else 0 for row in results]
signal_norm = np.array(signal_levels) / 4.0 

print(f"Точек: {len(lats)}")
print(f"SignalLevel: мин={min(signal_levels)}, макс={max(signal_levels)}")

scatter = plt.scatter(lons, lats, 
                     c=signal_norm,                  
                     cmap='RdYlGn',                 
                     s=100 * signal_norm + 30,         
                     vmin=0, vmax=1)                 

plt.xlabel('Долгота')
plt.ylabel('Широта')
plt.title(f'Качество сети (SignalLevel 0-4)\n'
          f'Точек: {len(lats)} | Средний уровень: {np.mean(signal_levels):.1f}')

plt.grid()

cbar = plt.colorbar(scatter, shrink=0.8, pad=0.02)
cbar.set_label('SignalLevel (0-4)')
cbar.set_ticks(np.linspace(0, 1, 5))  
cbar.set_ticklabels(['0\n(нет)', '1', '2', '3', '4\n(отлично)'])



counts = np.bincount(signal_levels, minlength=5)


plt.tight_layout()
plt.show(block=True)

cursor.close()
conn.close()
