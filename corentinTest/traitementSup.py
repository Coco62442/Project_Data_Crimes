import pandas as pd

# Charger le fichier CSV existant
df = pd.read_csv('dataCorrectedCSV/Services PN 2021.csv')

# Extraire la dernière ligne du DataFrame
keys = df.iloc[-1]

# Supprimer la dernière ligne du DataFrame
df = df[:-1]

# Définir les clés comme noms de colonnes
df.columns = keys

# Réinitialiser les index du DataFrame
df = df.reset_index(drop=True)

# Convertir toutes les colonnes en float pour effectuer la somme
df = df.apply(pd.to_numeric, errors='ignore')

# Calculer la somme des valeurs de chaque ligne, à l'exception de la première colonne
df['Total'] = df.iloc[:, 1:].sum(axis=1)



# Réinitialiser les index du DataFrame
df = df.reset_index(drop=True)

# Sauvegarder le DataFrame avec la colonne 'Total' ajoutée dans un nouveau fichier CSV
df.to_csv('Services PN 2021.csv', index=False)






# # Calculez la somme des lignes, en excluant la première colonne et les deux dernières lignes
# df['total'] = df.iloc[2:-2, 1:].sum(axis=1)

# # Enregistrez le DataFrame modifié dans le même fichier CSV
# df.to_csv('Services PN 2021.csv', index=False)

# # Vérifiez que le fichier a bien été enregistré
# print(f"Le fichier {votre_fichier.csv} a été mis à jour avec succès.")
