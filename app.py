# import geoviews as gv
# import geoviews.feature as gf
# import geopandas as gpd
# import numpy as np
# from geoviews import dim
# import matplotlib.pyplot as plt
# import numpy as np
# from shiny import ui, render, App

# # Create some random data
# t = np.linspace(0, 2 * np.pi, 1024)
# data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

# app_ui = ui.page_fixed(
#     ui.h2("Playing with colormaps"),
#     ui.markdown("""
#         This app is based on a [Matplotlib example][0] that displays 2D data
#         with a user-adjustable colormap. We use a range slider to set the data
#         range that is covered by the colormap.
# zazaeze
#         [0]: https://matplotlib.org/3.5.3/gallery/userdemo/colormap_interactive_adjustment.html
#     """),
#     ui.layout_sidebar(
#         ui.panel_sidebar(
#             ui.input_radio_buttons("cmap", "Colormap type",
#                 dict(viridis="Perceptual", gist_heat="Sequential", RdYlBu="Diverging")
#             ),
#             ui.input_slider("range", "Color range", -1, 1, value=(-1, 1), step=0.05),
#         ),
#         ui.panel_main(
#             ui.output_plot("plot")
#         )
#     )
# )

# def server(input, output, session):
#     @output
#     @render.plot
#     def plot():
#         # Lisez le fichier GeoJSON
#         gdf = gpd.read_file('originalData/departements-version-simplifiee.geojson')
#         # Créez une nouvelle figure Matplotlib
#         fig, ax = plt.subplots()

#         # Ajoutez la couche géographique à la figure
#         gdf.plot(ax=ax)

#         # Personnalisez la figure au besoin
#         ax.set_title('Votre titre')
#         ax.set_xlabel('Votre xlabel')
#         ax.set_ylabel('Votre ylabel')

#         # Affichez la figure
#         return fig


# app = App(app_ui, server)

import ipyleaflet as L
from htmltools import css
import pandas as pd
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, reactive_read, register_widget
import json
import geopandas as gpd

# Charger les données GeoJSON depuis le fichier
geojson_file = './originalData/departements-version-simplifiee.geojson'
data = gpd.read_file(geojson_file)

# Convert the GeoDataFrame to a GeoJSON dictionary
geojson_data = json.loads(data.to_json())

# # Lire le fichier CSV
# df = pd.read_csv('./dataCorrectedCSV/Services PN.csv')

# # Transverser les colonnes en lignes
# df = df.melt(id_vars=df.keys())

# # Effectuer une jointure spatiale basée sur la colonne commune
# result = df.combine_first(data)

# result.to_csv('./test.csv')

def choose_color(d):
        if d > 1000:
            return '#800026' 
        elif d > 500: 
            return '#BD0026'  
        elif d > 200:  
            return '#E31A1C'
        elif d > 100:  
            return '#FC4E2A'
        elif d > 50:  
            return '#FD8D3C'
        elif d > 20:  
            return '#FEB24C'
        elif d > 10:  
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
    
    # Initialize and display when the session starts (1)
    map = L.Map(center=(46.2861, 3.1631), zoom=5, scroll_wheel_zoom=True)
    
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    register_widget("map", map)

    # Create a GeoJSON layer and add it to the map (2)
    geojson_layer = L.GeoJSON(data=geojson_data)
    map.add_layer(geojson_layer)

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
