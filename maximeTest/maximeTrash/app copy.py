import ipyleaflet as L
from htmltools import css
from shiny import App, reactive, render, ui
from shinywidgets import output_widget, reactive_read, register_widget
import json
import geopandas as gpd
import plotly.express as px

# Charger les données GeoJSON depuis le fichier
geojson_file = './originalData/departements-version-simplifiee.geojson'
data = gpd.read_file(geojson_file)

# Convert the GeoDataFrame to a GeoJSON dictionary
geojson_data = json.loads(data.to_json())

# Charger le csv
df = pd.read_csv("../dataCorrectedCSV/Services PN.csv",
                   dtype={"fips": str})


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
    geojson_layer = L.GeoJSON(data=geojson_data, style=lambda feature: {
        'fillColor': choose_color(feature['2019']['crime']),
        'fillOpacity': 0.7,
        'color': 'black',
        'weight': 1,
    })
    geojson_layer = L.GeoJSON(data=geojson_data)
    map.add_layer(geojson_layer)

    # ...

    # Create a Plotly Express choropleth map
    fig = px.choropleth(df, geojson=counties, locations='fips', color='unemp',
                        color_continuous_scale="Viridis",
                        range_color=(0, 12),
                        scope="usa",
                        labels={'unemp':'unemployment rate'}
                        )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Convert the Plotly figure to HTML and integrate it into the Shiny UI
    fig_html = fig.to_html()
    shiny_fig = ui.div(htmltools.HTML(fig_html), style=css(display="block", width="100%"))

    # Add the Plotly figure to the Shiny UI
    app_ui = ui.page_fluid(
        ui.div(
            ui.input_slider("zoom", "Map zoom level", value=5, min=1, max=18),
            ui.output_ui("map_bounds"),
            shiny_fig,  # Add the Plotly figure here
            style=css(
                display="flex", justify_content="center", align_items="center", gap="2rem"
            ),
        ),
        output_widget("map"),
    )

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
