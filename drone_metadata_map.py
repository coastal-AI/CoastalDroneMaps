import pandas as pd
import geopandas as gpd
from shapely import wkt
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, CustomJS, Div, WheelZoomTool
from bokeh.layouts import row, column
from bokeh.models.tiles import WMTSTileSource
from bokeh.plotting import figure

# Load the data from the Excel file
data = pd.read_excel('data/0METADATA_DRON.xlsx')

# Ensure necessary columns exist
required_columns = ['decimalLongitude', 'decimalLatitude', 'footprintWKT', 'associatedMedia', 'eventID', 'eventDate', 'DRONE', 'GSD (cm/px)', 'INSTITUTION', 'CONTACT']
if not all(col in data for col in required_columns):
    raise ValueError(f"The data must contain {', '.join(required_columns)} columns.")

# Create a point GeoDataFrame and convert to EPSG:3857
point_gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['decimalLongitude'], data['decimalLatitude']), crs="EPSG:4326")
point_gdf = point_gdf.to_crs(epsg=3857)

# Create a polygon GeoDataFrame from footprintWKT and convert to EPSG:3857
poly_gdf = gpd.GeoDataFrame(data, geometry=data['footprintWKT'].apply(wkt.loads), crs="EPSG:4326")
poly_gdf = poly_gdf.to_crs(epsg=3857)

# Prepare ColumnDataSource for points (centroids) with additional fields
centroids_source = ColumnDataSource(data={
    'x': point_gdf.geometry.x,
    'y': point_gdf.geometry.y,
    'associatedMedia': data['associatedMedia'],
    'eventID': data['eventID'],
    'eventDate': data['eventDate'],
    'DRONE': data['DRONE'],
    'resolution': data['GSD (cm/px)'],  # Rename for clarity
    'INSTITUTION': data['INSTITUTION'],
    'CONTACT': data['CONTACT']
})

# Prepare data for polygons
xs = [list(geom.exterior.coords.xy[0]) for geom in poly_gdf.geometry]
ys = [list(geom.exterior.coords.xy[1]) for geom in poly_gdf.geometry]

# Create ColumnDataSource for polygons
polygons_source = ColumnDataSource(data={'xs': xs, 'ys': ys})

# Display an empty initial information in Divs (details as rows)
eventID_div = Div(text="<strong>Event ID: <strong>", width=600)
eventDate_div = Div(text="<strong>Event Date: <strong>", width=600)
drone_div = Div(text="<strong>Drone: <strong>", width=600)
resolution_div = Div(text="<strong>Resolution (cm/px): <strong>", width=600)
institution_div = Div(text="<strong>Institution: <strong>", width=600)
contact_div = Div(text="<strong>Contact: <strong>", width=600)
image_div = Div(text="<img src='' style='max-width: 100%; max-height: 600px; display: block;' />", width=600, height=600)  # Image moved to bottom

# Create the map plot with CartoLight tiles
tile_url = 'https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png'
tile_source = WMTSTileSource(url=tile_url)


map_figure = figure(
    x_axis_type="mercator",
    y_axis_type="mercator",
    tools="tap, wheel_zoom, pan, reset",
    width=700, height=700
)
map_figure.add_tile(tile_source)

# Add points and polygons to the map
map_figure.scatter('x', 'y', size=10, source=centroids_source, color='blue', alpha=0.6)
map_figure.patches('xs', 'ys', source=polygons_source, fill_alpha=0.2, line_width=2, fill_color="green")

# Set wheel_zoom as the active scroll tool
map_figure.toolbar.active_scroll = map_figure.select_one(WheelZoomTool)

# Define JavaScript callback to update the Divs when a point is clicked
callback = CustomJS(args=dict(source=centroids_source, image_div=image_div, eventID_div=eventID_div,
                              eventDate_div=eventDate_div, drone_div=drone_div, resolution_div=resolution_div,
                              institution_div=institution_div, contact_div=contact_div), code="""
    const selected_index = source.selected.indices[0];
    if (selected_index !== undefined) {
        const data = source.data;
        eventID_div.text = `<strong>Event ID:</strong> <span>${data['eventID'][selected_index]}</span>`;
        eventDate_div.text = `<strong>Event Date:</strong> <span>${data['eventDate'][selected_index]}</span>`;
        drone_div.text = `<strong>Drone:</strong> <span>${data['DRONE'][selected_index]}</span>`;
        resolution_div.text = `<strong>Resolution (cm/px):</strong> <span>${data['resolution'][selected_index]}</span>`;
        institution_div.text = `<strong>Institution:</strong> <span>${data['INSTITUTION'][selected_index]}</span>`;
        contact_div.text = `<strong>Contact:</strong> <span>${data['CONTACT'][selected_index]}</span>`;
        image_div.text = `<img src='${data['associatedMedia'][selected_index]}' style='max-width: 100%; max-height: 500px; display: block;' />`;
    }
""")
centroids_source.selected.js_on_change('indices', callback)

# Create combined main title and subtitle
main_title = Div(text="""
    <div style='width: 100%; text-align: left;'>
        <h1 style='font-size: 40px; margin-bottom: 5px;'>DRONE METADATA MAP</h1>
        <h3 style='font-size: 24px; margin-top: 0;'>Seagrass Ecology Group (IEO-CSIC)</h3>
        <p style='font-size: 16px;'>Dots represent aerial surveys. Polygons represent flight extent. Click centroids to display info and orthomosaic preview.</p>
        <br>
        <p style='font-size: 16px;'>For more info or download links please get in touch.</p>
        <br>
        <p style='font-size: 12px;'>License <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank">CC BY-NC 4.0</a> - Updated 22/10/2024</p>
        <br>
    </div>
""", width=1200)

# Arrange the layout with the map and the inverted table (details as rows, image at the bottom)
layout = column(
    main_title,
    row(
        map_figure,
        column(
            eventID_div,
            eventDate_div,
            drone_div,
            resolution_div,
            institution_div,
            contact_div,
            image_div  # Image at the bottom
        )
    )
)

# Output to an HTML file and show the result
output_file("output/index.html",title="Drone Metadata Map")
show(layout)