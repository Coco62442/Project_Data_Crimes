import geopandas as gpd
import pandas as pd
import json

# Charger le fichier Data
data_file = "../dataCorrectedCSV/Services PN.csv"
dataJ = pd.read_csv(data_file)

columnArray = ["Départements","Année","Code","971","972","973","974","976","987","988"]

