#########################################################################################################################################################
### Le traitementData travaille avec les fichiers .csv (plus facile à manipuler). Il faut exécuter le converter.py avant ###
#########################################################################################################################################################
import os
import pandas as pd

# Dossier contenant les fichiers CSV d'entrée
dossier_entree = "dataCSV"

# Dossier de sortie pour les fichiers corrigés
dossier_sortie = "dataCorrectedCSV"

# Créez le dossier de sortie s'il n'existe pas
if not os.path.exists(dossier_sortie):
    os.makedirs(dossier_sortie)

# Liste tous les fichiers CSV dans le dossier d'entrée
fichiers_entree = [f for f in os.listdir(dossier_entree) if f.endswith('.csv')]

# Créez une fonction personnalisée pour convertir en float ou garder les chaînes de caractères non numériques
def custom_to_numeric(value):
    try:
        return int(float(value))
    except (ValueError, TypeError):
        return str(value) + ' '
    
# Parcourez chaque fichier CSV dans le dossier d'entrée
for fichier in fichiers_entree:
    chemin_fichier_entree = os.path.join(dossier_entree, fichier)

    # Vérifiez si le fichier est vide
    if os.path.getsize(chemin_fichier_entree) == 0:
        print(f"Le fichier {fichier} est vide et sera ignoré.")
        continue
    
    # Charger le fichier CSV
    df = pd.read_csv(chemin_fichier_entree)

    # Renommer les colonnes en tant qu'entiers si possible
    for i in df.columns:
        try:
            entier = int(float(i))
            df.rename(columns={i: entier}, inplace=True)
        except ValueError:
            pass

    # Appliquer la fonction personnalisée à chaque élément du DataFrame
    df = df.map(custom_to_numeric)

    # Additionner les colonnes où la clé est identique
    df_grouped = df.T.groupby(level=0).sum().T

    # Enregistrer le DataFrame corrigé dans un fichier CSV avec le nom d'origine dans le dossier de sortie
    nom_fichier_sortie = os.path.splitext(fichier)[0] + '.csv'
    chemin_fichier_sortie = os.path.join(dossier_sortie, nom_fichier_sortie)
    df_grouped.to_csv(chemin_fichier_sortie, index=False)

#########################################################################################################################################################
####### La partie suivante concerne le fichier dataLess qui a servi de test pour créer le programme au dessus qui le fait pour toutes les données #######
#########################################################################################################################################################

# import pandas as pd

# # Récupérer le fichier .csv (dataLess.csv) dans le dossier (entrainementCSV)
# df = pd.read_csv("entrainementCSV/dataLess.csv")

# for i in df.keys():
#     try:
#         entier = int(float(i))
#         df.rename(columns={i : entier}, inplace=True)
#     except ValueError:
#         print(i)
        
# # Créez une fonction personnalisée pour convertir en float ou garder les chaînes de caractères non numériques
# def custom_to_numeric(value):
#     try:
#         return int(float(value))
#     except (ValueError, TypeError):
#         return str(value) + ' '

# # Appliquez la fonction personnalisée à chaque élément du DataFrame
# df = df.map(custom_to_numeric)

# # Additionner les colonnes où la clef est identique
# df_grouped = df.T.groupby(level=0).sum().T

# # Enregistrez le DataFrame dans un fichier CSV à côté
# df_grouped.to_csv('resultat.csv', index=False)
