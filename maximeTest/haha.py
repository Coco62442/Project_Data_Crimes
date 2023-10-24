import pandas as pd

file = pd.read_csv("colonne_code.csv")

for index, row in file.iterrows():
    # Imprimer les valeurs des colonnes "Type1" et "Type2" pour chaque ligne
    print("Type1:", row["Type1"],"  |   Type2:", row["Type2"] )