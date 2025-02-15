import folium
import pandas as pd
import geopandas as gpd
import json

# Load your population data.
# Assume the CSV has columns 'District' and 'Population'.
pop_data = pd.read_csv('Nepal_District_Populations_2021.csv')

# Load Nepal's district boundaries from a GeoJSON file.
# Here, we assume your file is named "gadm41_NPL_2.json"
nepal_districts = gpd.read_file('gadm41_NPL_2.json')

# Merge the population data with the GeoDataFrame.
# Adjust the merge keys as needed.
# For example, if the GeoJSON uses "NAME_2" for district names:
nepal_districts = nepal_districts.merge(pop_data, left_on='NAME_2', right_on='District')

# Optionally, inspect the merged data.
print(nepal_districts.head())

# Convert the GeoDataFrame to a GeoJSON string.
nepal_geojson = nepal_districts.to_json()

# Create a Folium map centered on Nepal.
m = folium.Map(location=[28.3949, 84.1240], zoom_start=7)

# Add a choropleth layer to the map.
folium.Choropleth(
    geo_data=nepal_geojson,
    name='Choropleth',
    data=pop_data,
    columns=['District', 'Population'],
    key_on='feature.properties.NAME_2',  # Adjust to match your GeoJSON property name
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population by District'
).add_to(m)

# Add a layer control panel.
folium.LayerControl().add_to(m)

# Save the map to an HTML file.
m.save('nepal_population_heatmap.html')

print("Map has been saved as 'nepal_population_heatmap.html'")
