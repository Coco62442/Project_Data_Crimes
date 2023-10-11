import pandas as pd
import json

# Charger le DataFrame à partir de vos données (remplacez cela par votre propre DataFrame)
data = pd.DataFrame({
    'year': [2019, 2019, 2020, 2020],
    'label': ['A', 'B', 'A', 'B'],
    'value': [10, 20, 15, 25]
})

# Charger le fichier Data
data_file = "../dataCorrectedCSV/Services PN.csv"
dataJ = pd.read_csv(data_file)

# Initialiser le dictionnaire JSON
json_data = {}

dep = 2
# Parcourir les lignes du DataFrame et ajouter les éléments au JSON
for index, row in dataJ.iterrows():
    year = row[1]
    label = row[0]
    value = row[2]
    
    # Si l'année n'existe pas encore dans le JSON, l'ajouter
    if year not in json_data:
        json_data[year] = {}
    
    # Ajouter le label et la valeur pour cette année
    json_data[year][label] = value

# Sauvegarder le JSON dans un fichier
with open('output.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print("Fichier JSON créé avec succès.")
