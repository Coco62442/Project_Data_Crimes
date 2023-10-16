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
    
# Créez deux DataFrames vides pour Services PN et Services GN
df_services_pn = pd.DataFrame()
df_services_gn = pd.DataFrame()

# Parcourez chaque fichier CSV dans le dossier d'entrée
for fichier in fichiers_entree:
    chemin_fichier_entree = os.path.join(dossier_entree, fichier)

    # Vérifiez si le fichier est vide
    if os.path.getsize(chemin_fichier_entree) == 0:
        print(f"Le fichier {fichier} est vide et sera ignoré.")
        continue
    
    # Charger le fichier CSV
    df = pd.read_csv(chemin_fichier_entree)
    
    # Renommer colonne "Départements" en "code"
    df.rename(columns={'Départements': 'code'}, inplace=True)
    
    # Filtrez les lignes en fonction d'une condition
    condition = df['code'] != 'Périmètres'
    df = df[condition]
    condition = ~df['code'].str.startswith("Libellé")
    df = df[condition]

    # Renommer les colonnes en tant qu'entiers si possible
    for i in df.columns:
        try:
            entier = int(float(i))
            df.rename(columns={i: entier}, inplace=True)
        except ValueError:
            # Si i correspond à la chaîne de caractère qui commence par "2A" ou "2B" alors on remplace par "2A" ou "2B"
            if i.startswith("2A") :
                df.rename(columns={i : "2A"}, inplace=True)
            elif i.startswith("2B"):
                df.rename(columns={i : "2B"}, inplace=True)
            else:
                pass

    # Appliquer la fonction personnalisée à chaque élément du DataFrame
    df = df.map(custom_to_numeric)

    # Additionner les colonnes où la clé est identique
    df_grouped = df.T.groupby(level=0).sum().T

    # Enregistrer le DataFrame corrigé dans un fichier CSV avec le nom d'origine dans le dossier de sortie
    nom_fichier_sortie = os.path.splitext(fichier)[0] + '.csv'
    chemin_fichier_sortie = os.path.join(dossier_sortie, nom_fichier_sortie)
    df_grouped.to_csv(chemin_fichier_sortie, index=False)
    
    # Extraire l'année à partir du nom du fichier (assumant que le nom suit un certain format)
    annee = fichier.split()[-1].split('.')[0]

    # Ajoutez une colonne "Année" avec la valeur extraite
    df_grouped['Year'] = annee
    
    # Vérifiez le type de service (PN ou GN) à partir du nom du fichier
    if "PN" in fichier:
        df_services_pn = pd.concat([df_services_pn, df_grouped], ignore_index=True)
    elif "GN" in fichier:
        df_services_gn = pd.concat([df_services_gn, df_grouped], ignore_index=True)

# Suppression des colonnes qui commencent par "Année"
df_services_pn = df_services_pn[df_services_pn.columns.drop(list(df_services_pn.filter(regex='^Année')))]
df_services_gn = df_services_gn[df_services_gn.columns.drop(list(df_services_gn.filter(regex='^Année')))]

# Remplacer les cases vides par la valeur 0
df_services_pn = df_services_pn.fillna(0)
df_services_gn = df_services_gn.fillna(0)

# Trier les colonnes du dataFrame en fonction de la colonne "code" puis de la colonne "Year" puis dans l'ordre croissant
df_services_pn = df_services_pn[['code', 'Year', '2A', '2B'] + sorted(df_services_pn.columns.difference(['code', 'Year', '2A', '2B']))]
df_services_gn = df_services_gn[['code', 'Year', '2A', '2B'] + sorted(df_services_gn.columns.difference(['code', 'Year', '2A', '2B']))]

# Trier les lignes du dataFrame en fonction de la colonne "Year"
df_services_pn = df_services_pn.sort_values(by=['Year'])
df_services_gn = df_services_gn.sort_values(by=['Year'])

# Renommer la colonne "Year" en "Année"
df_services_pn.rename(columns={'Year': 'Année'}, inplace=True)
df_services_gn.rename(columns={'Year': 'Année'}, inplace=True)

# Enregistrez les DataFrames dans deux fichiers CSV
df_services_pn.to_csv(os.path.join(dossier_sortie, 'Services PN.csv'), index=False)
df_services_gn.to_csv(os.path.join(dossier_sortie, 'Services GN.csv'), index=False)

#########################################################################################################################################################
####### La partie suivante concerne le fichier dataLess qui a servi de test pour créer le programme au dessus qui le fait pour toutes les données #######
#########################################################################################################################################################

# import pandas as pd

# # Récupérer le fichier .csv (dataLess.csv) dans le dossier (entrainementCSV)
# df = pd.read_csv("entrainementCSV/dataLess.csv")

# # Filtrez les lignes en fonction d'une condition
# condition = df['Départements'] != 'Périmètres'
# df = df[condition]
# condition = df['Départements'] != 'Libellé index \ CSP'
# df = df[condition]


# for i in df.keys():
#     try:
#         entier = int(float(i))
#         df.rename(columns={i : entier}, inplace=True)
#     except ValueError:
#         # Si i correspond à la chaîne de caractère qui commence par "2A" ou "2B" alors on remplace par "2A" ou "2B"
#         if i.startswith("2A") :
#             df.rename(columns={i : "2A"}, inplace=True)
#         elif i.startswith("2B"):
#             df.rename(columns={i : "2B"}, inplace=True)
#         else:
#             pass
        
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
# df_grouped.to_csv('entrainementCSV/resultat.csv', index=False)
