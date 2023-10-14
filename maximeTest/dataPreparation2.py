import pandas as pd

# Étape 1 : Charger un fichier xls
nom_fichier_xls = "../originalData/fichier_poplegale.xlsx"
xl = pd.ExcelFile(nom_fichier_xls)

# Étape 2 : Prendre chaque feuille du xls et les réunir dans un même dataframe
dataframes = []  # Une liste pour stocker les dataframes de chaque feuille

for nom_feuille in xl.sheet_names:
    annee = int(nom_feuille)  # Convertir le nom de la feuille en année (assurez-vous que les noms des feuilles sont des années valides)
    df = xl.parse(nom_feuille)
    df['Année'] = annee  # Ajouter la colonne "Année"
    dataframes.append(df)

# Concaténer les dataframes en un seul en ajoutant des labels aux colonnes
dataframe_final = pd.concat(dataframes, ignore_index=True, keys=xl.sheet_names)

# Étape 3 : Faire la somme des lignes avec les mêmes 2 premiers chiffres de la colonne "COM"
dataframe_final['Code'] = dataframe_final['COM'].astype(str).str[:2]  # Extraire les 2 premiers chiffres de la colonne "COM"
resultat = dataframe_final.groupby(['Année', 'Code'])['PMUN'].sum().reset_index()

# Étape 4 : Sauvegarder le dataframe dans un fichier .csv
nom_fichier_csv = "population_intermediaire_test.csv"
resultat.to_csv(nom_fichier_csv, index=False)


