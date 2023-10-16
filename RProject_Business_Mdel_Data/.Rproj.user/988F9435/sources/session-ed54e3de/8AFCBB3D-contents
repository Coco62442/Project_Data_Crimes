library(shiny)
library(dplyr)
library(leaflet)
library(sf)
library(geojsonsf)
library(RColorBrewer)

# Define UI for application that draws a histogram
ui <- fluidPage(

        titlePanel("Carte intéractive"),
        sidebarLayout(
          sidebarPanel(
            radioButtons(
              "selected_year",  # Nom de l'input
              "Sélectionnez une année :",
              choices = 2012:2021,  # Plage d'années
              selected = 2021  # Année par défaut sélectionnée
            )
          ),
        # Show a plot of the generated distribution
        mainPanel(
          leafletOutput("carteDprt", height = 800, width = 700)
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$carteDprt <- renderLeaflet({
      data_2021 <- read.csv("Services PN 2021.csv")
      
      # Gérer les valeurs NA dans la colonne "code" de data_2021
      data_2021 <- data_2021 %>%
        filter(!is.na(code)) %>%
        mutate(code = as.integer(code))
      #View(data_2021)
      
      # Lire les données geojson
      departements <- geojson_sf("departements.geojson")
      departements <- st_as_sf(departements)
      
      # Supprimer les zéros initiaux de la colonne "code" dans le data frame "departements"
      departements$code <- as.integer(departements$code)
      #View(departements)
      
      # Joindre les data frames en fonction de la colonne "code"
      result <- left_join(data_2021, departements, by = "code") %>%
        select(-nom)
      
      result <- st_as_sf(result)
      
      # Création d'une palette de couleurs personnalisée
      color_pal <- colorBin(palette = "viridis", domain = result$Total, reverse = TRUE, n = 5)
      
      # Afficher les régions sur une carte leaflet
      leaflet() %>% addTiles() %>%
        addPolygons(data = result, fillColor = ~color_pal(Total),
                    color = "black",
                    weight = 2,
                    fillOpacity = 0.5,
                    highlightOptions = highlightOptions(
                      color = "white",
                      weight = 2,
                      bringToFront = TRUE
                    )
        ) %>%
        addLegend(position = "bottomright", pal = colorBin("viridis", result$Total, reverse = TRUE, n = 5),
                  values = result$Total, title = "Total", opacity = 0.8) %>%
        addControl("Carte du total de crimes par rapport aux départements français")
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
