import geopandas as gpd
import pandas as pd
import json

# Charger le fichier GeoJSON
geojson_file = "../originalData/departements-version-simplifiee.geojson"
geoJ = gpd.read_file(geojson_file)

print(geoJ.head())
