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
    SELECT Lat, Lon, RSRP, Cells 
    FROM telephony 
""")
results = cursor.fetchall()

lats = [float(row[0]) for row in results]
lons = [float(row[1]) for row in results]


rsrp_values = [float(row[2]) for row in results if row[2] is not None]


if not rsrp_values:
    rsrp_values = [-120.0]

rsrp_min = min(min(rsrp_values), -140.0)
rsrp_max = max(max(rsrp_values), -80.0)

rsrp = np.array([float(v) if v is not None else np.mean(rsrp_values)
                 for v in [row[2] for row in results]])


rsrp_norm = (rsrp - rsrp_min) / (rsrp_max - rsrp_min)
rsrp_norm = np.clip(rsrp_norm, 0, 1)

print(f"Точек: {len(lats)}")

scatter = plt.scatter(
    lons,
    lats,
    c=rsrp_norm,         
    cmap='RdYlGn',       
    s=100 * rsrp_norm + 30,
    vmin=0, vmax=1
)

plt.xlabel('Долгота')
plt.ylabel('Широта')
plt.title(
    f'Качество сети\n'
    f'Точек: {len(lats)}'
)

plt.grid()

cbar = plt.colorbar(scatter, shrink=0.8, pad=0.02)
cbar.set_label('RSRP')

ticks_norm = np.linspace(0, 1, 5)
ticks_rsrp = rsrp_min + ticks_norm * (rsrp_max - rsrp_min)
cbar.set_ticks(ticks_norm)
cbar.set_ticklabels([f'{v:.0f} дБм' for v in ticks_rsrp])

plt.tight_layout()
plt.show()

cursor.close()
conn.close()
