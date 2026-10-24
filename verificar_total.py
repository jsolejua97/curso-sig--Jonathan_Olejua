import requests

url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

params = {
    "where": "1=1",
    "returnCountOnly": "true",
    "f": "json"
}

try:
    respuesta = requests.get(url, params=params, timeout=60)
    respuesta.raise_for_status()

    datos = respuesta.json()

    print("Total de veredas en el servicio:", datos.get("count"))
    print("Veredas descargadas:", 1713)

    if datos.get("count") == 1713:
        print("Verificación: coincide el total.")
    else:
        print("Verificación: debemos revisar si faltan registros.")

except Exception as error:
    print("Error durante la verificación:", error)