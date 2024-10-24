import pandas as pd
from shapely import wkt
import json

# Load the Excel file
file_path = '0METADATA_DRON.xlsx'
data = pd.read_excel(file_path)

# Select relevant columns for conversion to JSON
relevant_columns = ['eventID', 'eventDate', 'DRONE', 'GSD (cm/px)', 'INSTITUTION', 'CONTACT', 'decimalLatitude', 'decimalLongitude', 'footprintWKT']

# Ensure the columns are in the correct format for Leaflet
data_filtered = data[relevant_columns].copy()

# Rename columns to match the JSON structure
data_filtered.rename(columns={
    'GSD (cm/px)': 'resolution',
    'decimalLatitude': 'latitude',
    'decimalLongitude': 'longitude',
    'DRONE': 'drone',
    'INSTITUTION': 'institution',
    'CONTACT': 'contact'
}, inplace=True)

# Generate the associatedMedia URL
associatedMedia_url = 'https://filedn.eu/lxdSetOgU6G8FNMH4dxBDJQ/coastalDroneMetadataMap/'
data_filtered['associatedMedia'] = associatedMedia_url + data_filtered['eventID'].astype(str) + '_image.jpg'

# Convert footprintWKT to list of coordinate pairs for polygons (Leaflet expects [latitude, longitude])
def convert_wkt_to_coordinates(wkt_str):
    geom = wkt.loads(wkt_str)
    return [(coord[1], coord[0]) for coord in geom.exterior.coords]

data_filtered['footprint'] = data_filtered['footprintWKT'].apply(convert_wkt_to_coordinates)

# Drop the original footprintWKT column
data_filtered.drop(columns=['footprintWKT'], inplace=True)

# Convert the DataFrame to a JSON-like structure
json_data = data_filtered.to_dict(orient='records')

# Prepare the JavaScript variable with data
js_variable = f"var data = {json.dumps(json_data, indent=4)};"

# Save to a .js file
output_js_path = '0METADATA_DRON.js'
with open(output_js_path, 'w') as js_file:
    js_file.write(js_variable)


# Print the path to the JSON file
print(f"JSON file saved to: {output_js_path}")
