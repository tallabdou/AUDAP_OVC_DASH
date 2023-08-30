import geopandas as gpd
import folium
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from read_data_colleges_palois import gdf_ut_college
# Assuming gdf_ut_college is your DataFrame with the structure you provided

def map_colleges_ut_palois():
    # Convert the DataFrame to a GeoDataFrame
    gdf = gpd.GeoDataFrame(gdf_ut_college, geometry='geometry_x')

    # Create a dictionary to store color mapping based on unique libetab values
    unique_libetab_values = gdf['libetab'].unique()

    # Generate a colormap based on unique libetab values
    num_colors = len(unique_libetab_values)
    colormap = plt.cm.get_cmap('Set1', num_colors)

    libetab_color_mapping = {
        value: mcolors.to_hex(colormap(i))
        for i, value in enumerate(unique_libetab_values)
    }

    # Create a Folium map centered at a specific location
    m = folium.Map(location=[gdf['geometry_y'].y.mean(), gdf['geometry_y'].x.mean()], zoom_start=12)

    # Add polygons (geometry_x) with color based on libetab to the map
    for idx, row in gdf.iterrows():
        libetab_value = row['libetab']
        color = libetab_color_mapping[libetab_value]
        geojson = folium.GeoJson(
            row['geometry_x'],
            style_function=lambda feature, color=color: {
                'fillColor': color,
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.5,
            }
        )
        popup_text = f"UT: {row['ut_nom']}<br>Collège: {row['libetab']}<br>IPS UT: {row['ips_ut']}"
        folium.Popup(popup_text).add_to(geojson)
        geojson.add_to(m)

    # Add points (geometry_y) to the map without duplication
    added_points = {}

    for idx, row in gdf.iterrows():
        point_location = (row['geometry_y'].y, row['geometry_y'].x)
        if point_location not in added_points:
            polygon_index = gdf.index[gdf['geometry_y'] == row['geometry_y']].tolist()[0]
            color = libetab_color_mapping.get(gdf.at[polygon_index, 'libetab'], 'gray')
            icon_html = f'<i class="fa fa-graduation-cap fa-3x" style="color:{color};"></i>'
            folium.Marker(
                location=point_location,
                icon=folium.DivIcon(html=icon_html),
                popup=row['college_nom']
            ).add_to(m)
            added_points[point_location] = True

    # Add the specific point and label to the map
    specific_point_location = (43.30485, -0.36425)
    icon_html = f'<i class="fa fa-graduation-cap fa-3x" style="color:white;"></i>'
    folium.Marker(
        location=specific_point_location,
        icon=folium.DivIcon(html=icon_html),
        popup="Collège Pierre Emmanuel"
    ).add_to(m)
    
    # Add Layer Control to the map
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    return m