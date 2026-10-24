
import geopandas as gpd
import pandas as pd

# 1. Leer el archivo completo de veredas
ruta = "datos/veredas_boyaca.geojson"
gdf = gpd.read_file(ruta)

print("Total de veredas:", len(gdf))
print("Total de municipios:", gdf["NOMB_MPIO"].nunique())

# 2. Contar veredas por municipio
por_municipio = (
    gdf.groupby("NOMB_MPIO")
    .size()
    .sort_values(ascending=False)
)

print("\nTOP 10 MUNICIPIOS CON MÁS VEREDAS:")
print(por_municipio.head(10).to_string())

# 3. Reproyectar a un sistema de coordenadas en metros
gdf_m = gdf.to_crs(epsg=9377)

# 4. Calcular el área en hectáreas
gdf_m["area_ha_calculada"] = gdf_m.geometry.area / 10000

# 5. Mostrar las cinco veredas de mayor área
top_5 = gdf_m.nlargest(5, "area_ha_calculada")

print("\nTOP 5 VEREDAS CON MAYOR ÁREA:")
print(
    top_5[
        ["NOMB_MPIO", "NOMBRE_VER", "area_ha_calculada"]
    ].to_string(index=False)
)

# 6. Guardar el resultado en formato GeoPackage
salida = "datos/veredas_area.gpkg"
gdf_m.to_file(salida, driver="GPKG")

print("\nArchivo guardado en:", salida)
