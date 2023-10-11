import geopandas as gpd
import pandas as pd
import json

# Charger le fichier GeoJSON
geojson_file = "../originalData/departements-version-simplifiee.geojson"
temp = open(geojson_file)
geoJ = json.load(temp)

# Charger le fichier Data
data_file = "../dataCorrectedCSV/Services PN.csv"
dataJ = pd.read_csv(data_file)

columnArray = ["Départements","Année","Code","971","972","973","974","976","987","988"]

for column in dataJ.columns:
  if column not in columnArray:
    littleJson = {}

    for i in range(0,len(dataJ[column])):
      year = str(dataJ.iat[i,1])
      label = dataJ.iat[i,0]
      value = dataJ[column][i]
      
      # Si l'année n'existe pas encore dans le JSON, l'ajouter
      if year not in littleJson:
          littleJson[year] = {}
        
      littleJson[year][label] = int(value)

    for j in range(0,len(geoJ["features"])):
      if column in ["2A","2B"]:
        if str(geoJ["features"][j]["properties"]["code"]) == str(column):
          geoJ["features"][j]["properties"]["years"] = littleJson
      else:
        if geoJ["features"][j]["properties"]["code"] not in ["2A","2B"]:
          if int(geoJ["features"][j]["properties"]["code"]) == int(column):
            geoJ["features"][j]["properties"]["years"] = littleJson
    
# Sauvegarder le dernier dictionnaire littleJson
with open(f'../dataCorrectedGeoJSON/cleanGeoJSON.geojson', 'w') as json_file:
  json.dump(geoJ, json_file, indent=4)