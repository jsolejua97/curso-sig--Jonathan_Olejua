
import requests
import geopandas as gpd
from pathlib import Path

url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

params = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "true",
    "outSR": "4326",
    "f": "geojson",
    "resultRecordCount": 2000
}

try:
    respuesta = requests.get(url, params=params, timeout=120)
    respuesta.raise_for_status()

    datos = respuesta.json()

    if datos.get("type") != "FeatureCollection":
        raise ValueError(f"Respuesta inesperada: {datos}")

    gdf = gpd.GeoDataFrame.from_features(
        datos["features"],
        crs="EPSG:4326"
    )

    # Crear carpeta de datos si no existe
    carpeta = Path("datos")
    carpeta.mkdir(exist_ok=True)

    salida = carpeta / "veredas_boyaca.geojson"
    gdf.to_file(salida, driver="GeoJSON")

    print("Descarga completada.")
    print("Veredas recibidas:", len(gdf))
    print("Archivo guardado en:", salida.resolve())
    print("Campos:", gdf.columns.tolist())

except Exception as error:
    print("Error durante la descarga:", error)
