
import requests

url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

base = {
    "where": "1=1",
    "outFields": "NOMB_MPIO,NOMBRE_VER",
    "outSR": "4326",
    "f": "geojson"
}

features = []
offset = 0
bloque = 1000

while True:
    params = {
        **base,
        "resultOffset": offset,
        "resultRecordCount": bloque
    }

    respuesta = requests.get(url, params=params, timeout=30)
    respuesta.raise_for_status()
    datos = respuesta.json()

    nuevos = datos.get("features", [])
    features += nuevos

    print(f"Offset {offset}: +{len(nuevos)} (total {len(features)})")

    if len(nuevos) < bloque:
        break

    offset += bloque

municipios = {
    f["properties"]["NOMB_MPIO"]
    for f in features
    if f.get("properties", {}).get("NOMB_MPIO")
}

print("\nTOTAL DE VEREDAS:", len(features))
print("MUNICIPIOS DISTINTOS:", len(municipios))
