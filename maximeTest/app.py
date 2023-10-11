import ipyleaflet as L
from htmltools import css
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, reactive_read, register_widget
import json
import geopandas as gpd

# Charger les données GeoJSON depuis le fichier
geojson_file = './dataCorrectedGeoJSON/cleanGeoJSON.geojson'
data = gpd.read_file(geojson_file)

# Convert the GeoDataFrame to a GeoJSON dictionary
geojson_data = json.loads(data.to_json())
        

app_ui = ui.page_fluid(
    ui.div(
        ui.input_slider("zoom", "Map zoom level", value=5, min=1, max=18),
        ui.output_ui("map_bounds"),
        ui.input_select(
            "year",
            "Choose a year:",
            {
                "2012":"2012",
                "2013":"2013",
                "2014":"2014",
                "2015":"2015",
                "2016":"2016",
                "2017":"2017",
                "2018":"2018",
                "2019":"2019",
                "2020":"2020",
                "2021":"2021",
                "2022":"2O22"
            },
        ),
        ui.input_select(
            "criterion",
            "Choose a criterion:",
            {
                "Autres faux documents administratifs ":"Autres faux documents administratifs ",
                "Travail clandestin ":"Travail clandestin ",
            },
        ),
        style=css(
            display="flex", justify_content="center", align_items="center", gap="2rem"
        ),
    ),
    output_widget("map"),
)


def server(input, output, session):
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
        
    # Extract the value from the GeoJSON properties
    def get_value(x):
        return x["properties"]["years"][input.year][input.criterion]
    
    def get_color(x):
        value = get_value(x)
        return choose_color(value)
    
    def basic_color():
        return '#FFEDA0'
    # Initialize and display when the session starts (1)
    map = L.Map(center=(46.2861, 3.1631), zoom=5, scroll_wheel_zoom=True)
    
    # Add a distance scale
    map.add_control(L.leaflet.ScaleControl(position="bottomleft"))
    register_widget("map", map)

    # Create a GeoJSON layer and add it to the map
    geojson_layer = L.GeoJSON(data=geojson_data, style={
        'fillColor': basic_color(),
        # 'fillColor': get_color,
        # 'fillColor': if x["properties"]["years"][input.year][input.criterion] > 2 return '#800026' else return '#FFEDA0',
        'fillOpacity': 0.7,
        'color': 'black',
        'weight': 1,
    })
    map.add_layer(geojson_layer)

    # geojson_layer = L.GeoJSON(data=geojson_data)
    # map.add_layer(geojson_layer)

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
