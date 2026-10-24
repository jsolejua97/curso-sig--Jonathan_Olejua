
import json
import pandas as pd

# Ruta del archivo GeoJSON
ruta = r"C:\Users\DELLPHOTO\servicios_sig_y_websites\curso-sig\datos\provincias_boyaca.geojson"

# Leer el archivo GeoJSON
with open(ruta, "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

# Convertir las propiedades de cada municipio en una tabla
municipios = pd.DataFrame(
    [entidad["properties"] for entidad in datos["features"]]
)

# Contar municipios por provincia
conteo = municipios["provincia"].value_counts().sort_index()

# Mostrar resultados
print("Total de municipios:", len(municipios))
print("Total de valores distintos:", municipios["provincia"].nunique())
print("\nMunicipios por provincia:")
print(conteo.to_string())
