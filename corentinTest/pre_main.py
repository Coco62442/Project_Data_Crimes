# import pandas as pd

# # Charger le premier fichier CSV (fichier de données)
# df1 = pd.read_csv('dataForR/Services GN 2020.csv')

# # Charger le deuxième fichier CSV (correspondances entre les clés)
# df2 = pd.read_csv('etiquetage_categories.csv', sep=';')

# # Nettoyer les noms de colonnes en supprimant les espaces à la fin
# df1.columns = df1.columns.str.strip()

# # Créer un dictionnaire de correspondance entre les anciennes et les nouvelles clés
# correspondance = dict(zip(df2.keys(), df2.iloc[0]))

# # Obtenez la liste des noms de colonnes qui ne correspondent pas aux clés dans le dictionnaire
# noms_non_correspondants = set(df1.columns).difference(correspondance.keys())

# # Affichez les noms de colonnes qui ne correspondent pas
# print("Noms de colonnes non correspondants : ", noms_non_correspondants)

# # Renommer les clés dans le premier DataFrame en utilisant le dictionnaire de correspondance
# df1 = df1.rename(columns=correspondance)

# # Suppression des colonnes qui où la key commence par "Index"
# df1 = df1.drop(columns=[col for col in df1.columns if col.startswith('Index')])

# # Nettoyer les noms de colonnes en supprimant les espaces à la fin
# df1.columns = df1.columns.str.strip()

# # Groupement des colonnes ayant le même nom et somme de leurs valeurs
# df1 = df1.T.groupby(level=0).sum().T

# # Enregistrez le DataFrame résultant dans un nouveau fichier CSV
# df1.to_csv('fichier1_modifie.csv', index=False)


import os
import pandas as pd
import re

# Dossier contenant les fichiers CSV d'entrée
dossier_entree = "dataCorrectedCSV"

# Dossier de sortie pour les fichiers corrigés
dossier_sortie = "dataForRTest"

# Charger le deuxième fichier CSV (correspondances entre les clés)
df_etiquetage = pd.read_csv('etiquetage_categories.csv', sep=';')

# Créez le dossier de sortie s'il n'existe pas
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

# Liste tous les fichiers CSV dans le dossier d'entrée
fichiers_entree = [f for f in os.listdir(dossier_entree) if f.endswith('.csv')]

for i in fichiers_entree:
    
    if i != "Services PN 2021.csv":
        continue
        
    df = pd.read_csv(dossier_entree + '/' + i)

    # Transposer le DataFrame
    df_transpose = df.T

    # Utilisez la première ligne (l'en-tête) du DataFrame d'origine comme nouvelle colonne
    df_transpose[0] = df.columns

    # Réindexez le DataFrame pour obtenir les bonnes étiquettes de ligne
    df_transpose = df_transpose.reset_index(drop=True)

    # Assurez-vous que la première ligne du DataFrame transposé est correcte
    df_transpose.columns = df_transpose.iloc[0]

    # Supprimez la première ligne, car elle est maintenant l'en-tête des colonnes
    df_transpose = df_transpose.iloc[1:]

    # Insérez une première ligne vide au début du DataFrame
    df_transpose.loc[-1] = [None] * len(df_transpose.columns)

    # Réorganisez l'index pour avoir -1 en haut
    df_transpose = df_transpose.sort_index()

    # Réinitialisez l'index du DataFrame final
    df_transpose.reset_index(drop=True, inplace=True)

    df_transpose.iloc[0] = df_transpose.keys()

    # Utilisez la dernière ligne comme noms de colonnes
    df_transpose.columns = df_transpose.iloc[-1]

    # Supprimez la dernière ligne du DataFrame
    df_transpose = df_transpose.drop(df_transpose.index[[-1, -2]])

    # Réinitialisez l'index si nécessaire
    df_transpose = df_transpose.reset_index(drop=True)
    
    # Utilisez une expression régulière pour extraire l'année
    # annee_match = re.search(r'\b\d{4}\b', fichiers_entree[13])
    annee_match = re.search(r'\b\d{4}\b', i)

    if annee_match:
        annee_extraite = annee_match.group()
        print("Année extraite :", annee_extraite)
    else:
        annee_extraite = "XXXX"
        print("Aucune année trouvée dans le nom de fichier.")
        continue

    # Créez un nouveau DataFrame pour la première colonne "Année" avec toutes les valeurs "2020"
    annee = pd.DataFrame({'Année': [annee_extraite] * len(df_transpose)})
    
    # Concaténez les deux DataFrames
    df_transpose = pd.concat([df_transpose, annee], axis=1)

    # Réinitialisez l'index
    df_transpose = df_transpose.reset_index(drop=True)
    
    # Nettoyer les noms de colonnes en supprimant les espaces à la fin
    df_transpose.columns = df_transpose.columns.str.strip()

    # Créer un dictionnaire de correspondance entre les anciennes et les nouvelles clés
    correspondance = dict(zip(df_etiquetage.keys(), df_etiquetage.iloc[0]))

    # Obtenez la liste des noms de colonnes qui ne correspondent pas aux clés dans le dictionnaire
    noms_non_correspondants = set(df_transpose.columns).difference(correspondance.keys())

    # Affichez les noms de colonnes qui ne correspondent pas
    print("Noms de colonnes non correspondants : ", noms_non_correspondants)

    # Renommer les clés dans le premier DataFrame en utilisant le dictionnaire de correspondance
    df_transpose = df_transpose.rename(columns=correspondance)

    # Suppression des colonnes qui où la key commence par "Index"
    df_transpose = df_transpose.drop(columns=[col for col in df_transpose.columns if col.startswith('Index')])

    # Nettoyer les noms de colonnes en supprimant les espaces à la fin
    df_transpose.columns = df_transpose.columns.str.strip()

    # Convertissez les valeurs en nombres (si elles ne le sont pas déjà)
    df_transpose = df_transpose.apply(pd.to_numeric, errors='coerce')

    # Groupez les colonnes identiques et faites la somme des valeurs
    df_transpose = df_transpose.T.groupby(level=0).sum().T

    # Enregistrez le DataFrame résultant dans un nouveau fichier CSV
    df_transpose.to_csv(dossier_sortie + '/' + i, index=False)