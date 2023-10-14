import ipyleaflet as L
from htmltools import css
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, reactive_read, register_widget
import json
import geopandas as gpd
import matplotlib.pyplot as plt

# Charger le fichier GeoJSON
geojson_file = "../originalData/departements-version-simplifiee.geojson"
geoJ = gpd.read_file(geojson_file)

# Convertir le GeoDataFrame en GeoJSON
geojson_data = geoJ.__geo_interface__


def choose_color(d):
        if d > 250:
            return '#800026' 
        elif d > 200: 
            return '#BD0026'  
        elif d > 150:  
            return '#E31A1C'
        elif d > 100:  
            return '#FC4E2A'
        elif d > 75:  
            return '#FD8D3C'
        elif d > 50:  
            return '#FEB24C'
        elif d > 25:  
            return '#FED976' 
        else:
            return '#FFEDA0'

app_ui = ui.page_fluid(
    ui.div(
        ui.input_slider("zoom", "Map zoom level", value=5, min=1, max=18),
        ui.output_ui("map_bounds"),
        style=css(
            display="flex", justify_content="center", align_items="center", gap="2rem"
        ),
    ),
    output_widget("map"),
)


def server(input, output, session):
    
   # Créer la carte choroplèthe
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    @reactive.Effect
    def _():
        # Afficher la carte choroplèthe
        geoJ.plot(column=input., cmap='coolwarm', ax=ax, legend=True)

    # Personnaliser la carte
    ax.set_title('Carte Choroplèthe en fonction des valeurs')
    ax.axis('off')

    # Afficher la carte
    plt.show()
    
    # When the slider changes, update the map's zoom attribute (2)
    @reactive.Effect
    def _():
        map.zoom = input.zoom()

    # When zooming directly on the map, update the slider's value (2 and 3)
    @reactive.Effect
    def _():
        ui.update_slider("zoom", value=reactive_read(map, "zoom"))

    # Everytime the map's bounds change, update the output message (3)
    @output
    @render.ui
    def map_bounds():
        center = reactive_read(map, "center")
        if len(center) == 0:
            return

        lat = round(center[0], 4)
        lon = (center[1] + 180) % 360 - 180
        lon = round(lon, 4)

        return ui.p(f"Latitude: {lat}", ui.br(), f"Longitude: {lon}")
    


app = App(app_ui, server)
