
import requests

url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

params = {
    "where": "1=1",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "returnGeometry": "false",
    "resultRecordCount": 5,
    "f": "json"
}

try:
    respuesta = requests.get(url, params=params, timeout=30)
    print("Estado HTTP:", respuesta.status_code)
    respuesta.raise_for_status()

    datos = respuesta.json()
    print("Registros recibidos:", len(datos.get("features", [])))
    print("Primer registro:")
    print(datos.get("features", [{}])[0].get("attributes", {}))

except requests.exceptions.RequestException as error:
    print("Error de conexión:", error)
