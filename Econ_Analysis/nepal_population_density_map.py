import folium
import pandas as pd
import geopandas as gpd

# Load your population data.
pop_data = pd.read_csv('Nepal_District_Populations_2021_renamed.csv')
pop_data['District'] = pop_data['District'].str.strip().str.lower()

# Load Nepal's district boundaries from the GeoJSON file.
nepal_districts = gpd.read_file('gadm41_NPL_3.json')
nepal_districts['NAME_3'] = nepal_districts['NAME_3'].str.strip().str.lower()

# Merge the population data with the GeoDataFrame using "NAME_3"
nepal_districts = nepal_districts.merge(pop_data, left_on='NAME_3', right_on='District')

# Inspect the merged data.
print(nepal_districts.head())
print("Number of merged rows:", len(nepal_districts))

# Convert the merged GeoDataFrame to GeoJSON.
nepal_geojson = nepal_districts.to_json()

# Create a Folium map centered on Nepal.
m = folium.Map(location=[28.3949, 84.1240], zoom_start=7)

# Add a choropleth layer to the map using the appropriate population column.
folium.Choropleth(
    geo_data=nepal_geojson,
    name='Choropleth',
    data=pop_data,
    columns=['District', 'Population_2021'],  # Use your actual population column name.
    key_on='feature.properties.NAME_3',        # Changed to "NAME_3"
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
