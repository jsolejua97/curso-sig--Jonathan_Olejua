
import json
from collections import Counter

# Ruta del archivo GeoJSON
ruta = r"C:\Users\DELLPHOTO\servicios_sig_y_websites\curso-sig\datos\provincias_boyaca.geojson"

# Leer el archivo
with open(ruta, "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

# Obtener la provincia de cada municipio
provincias = [
    entidad["properties"]["provincia"]
    for entidad in datos["features"]
]

# Contar municipios por provincia
conteo = Counter(provincias)

# Mostrar resultados
print("Total de municipios:", len(datos["features"]))
print("Total de provincias distintas:", len(conteo))
print("\nMunicipios por provincia:")

for provincia, cantidad in sorted(conteo.items()):
    print(f"{provincia}: {cantidad}")
