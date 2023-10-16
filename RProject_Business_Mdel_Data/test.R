library(dplyr)

data_2021 <- read.csv("Services PN 2021.csv")

# Lire les données geojson
departements <- geojson_sf("departements-version-simplifiee.geojson")

# Joindre les data frames en fonction de la colonne "code"
result <- left_join(data_2021, departements, by = "code") %>%
  select(-nom)