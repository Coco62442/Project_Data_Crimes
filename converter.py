### Convertit les feuilles présentent dans le fichier .xlsx en .csv ###
### Dans un dossier originalData il faut mettre le fichier .xlsx et le renommer data ###
### Le lien pour le télécharger est : https://www.data.gouv.fr/fr/datasets/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012/#/resources ###

import pandas as pd


# Nom du fichier de données
fileName = "originalData/data.xlsx"
# Nom des feuilles de données souhaitées

df = pd.read_excel(fileName, sheet_name=None)

for sheetName in df.keys():
    df[sheetName].to_csv("dataCSV/" + sheetName + ".csv", index=False)

print("Conversion terminée")