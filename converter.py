#########################################################################################################################################################
### Convertit les feuilles présentent dans le fichier .xlsx en .csv ###
### Dans un dossier originalData il faut mettre le fichier .xlsx et le renommer data ###
### Le lien pour le télécharger est : https://www.data.gouv.fr/fr/datasets/crimes-et-delits-enregistres-par-les-services-de-gendarmerie-et-de-police-depuis-2012/#/resources ###
#########################################################################################################################################################

import os
import pandas as pd


# Nom du fichier de données
fileName = "originalData/data.xlsx"
# Nom du dossier de sortie
dossier_sortie = "dataCSV/"

df = pd.read_excel(fileName, sheet_name=None)

# Créez le dossier de sortie s'il n'existe pas
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

for sheetName in df.keys():
    df[sheetName].to_csv(dossier_sortie + sheetName + ".csv", index=False)

print("Conversion terminée")

#########################################################################################################################################################
####### La partie suivante concerne le fichier dataLess qui a servi de test pour créer le programme au dessus qui le fait pour toutes les données #######
#########################################################################################################################################################


# import os
# import pandas as pd


# # Nom du fichier de données
# fileName = "entrainementCSV/dataLess.xlsx"
# # Nom du dossier de sortie
# dossier_sortie = "entrainementCSV/"

# df = pd.read_excel(fileName, sheet_name=None)

# # Créez le dossier de sortie s'il n'existe pas
# if not os.path.exists(dossier_sortie):
#     os.makedirs(dossier_sortie)

# for sheetName in df.keys():
#     df[sheetName].to_csv(dossier_sortie + "dataLess.csv", index=False)

# print("Conversion terminée")