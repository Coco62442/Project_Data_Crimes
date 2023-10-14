import pandas as pd
import json

# Étape 1 : Charger le fichier CSV
nom_fichier_csv = "population_intermediaire_test.csv"  # Spécifiez le chemin complet si nécessaire
df = pd.read_csv(nom_fichier_csv)

# Etape 2 : Charger le fichier GeoJSON
geojson_file = "../dataCorrectedGeoJSON/cleanGeoJSON.geojson"
temp = open(geojson_file)
geoJ = json.load(temp)


def addPopulation(year, code, value):
  year = str(year)
  code = str(code)
  for j in range(0,len(geoJ["features"])):
    if code in ["2A","2B"]:
      if str(geoJ["features"][j]["properties"]["code"]) == str(code):
        geoJ["features"][j]["properties"]["years"][year]["population"] = value
    else:
      if geoJ["features"][j]["properties"]["code"] not in ["2A","2B"]:
        if int(geoJ["features"][j]["properties"]["code"]) == int(code):
          geoJ["features"][j]["properties"]["years"][year]["population"] = value


# Étape 2 : Itérer sur toutes les lignes
for index, row in df.iterrows():
    year = row['Année']
    code = row['Code']
    value = row['PMUN']
    
    # Faites ici ce que vous souhaitez faire avec chaque ligne
    # print(f"Année: {annee}, Code: {deux_premiers_chiffres}, Valeur: {valeur}")
    addPopulation(year,code,value)

# Sauvegarder le dernier dictionnaire littleJson
with open(f'../dataCorrectedGeoJSON/cleanGeoJSON2.geojson', 'w') as json_file:
  json.dump(geoJ, json_file, indent=4)
