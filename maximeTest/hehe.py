import pandas as pd

file = pd.read_csv('../dataCorrectedCSV/Services PN 2021.csv')

print(file['code'])
# file['new_type'] = "null"

# df = file[['code','new_type']]
df = file['code']

# Créer une nouvelle colonne "new_type" avec des valeurs par défaut "null"

# Sauvegarder la colonne "code" dans un fichier CSV
df.to_csv("colonne_code.csv", index=False)
