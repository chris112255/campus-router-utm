import pandas as pd
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString, Point
import streamlit as st
from streamlit_folium import st_folium
import folium

@st.cache_data
def get_map_data(path_coords):
    line = LineString(path_coords)
    gdf = gpd.GeoDataFrame(geometry=[line], crs="EPSG:26917")
    return gdf.to_crs(epsg=4326) # Leaflet/explore needs Lat/Lon (4326)

def calculate_weight(start, end, edge_data):
    weighted_total = edge_data.get('length') * (1 + edge_data.get('avg_slope')/100)
    return weighted_total

df = pd.read_csv('paths.csv')
G = nx.Graph()

all_points = []

for index, row in df.iterrows():
    all_points.append([row.start_x, row.start_y])

    start = (row.start_x, row.start_y, row.start_z)
    end = (row.end_x, row.end_y, row.end_z)
    
    G.add_edge(start, end, name=row.name, avg_slope=row.slope_avg, length=row.length)

start_node = list(G.nodes)[0]
end_node = list(G.nodes)[100]

shortest_path = nx.shortest_path(G, start_node, end_node, weight=calculate_weight)

# 2. Render in Streamlit
st.title("My Route Mapper")

# Generate/Get your path
path_gdf = get_map_data(shortest_path)

# 3. Create the interactive map

center = [43.5494114, -79.6637835]

m = folium.Map(center, zoom_start=16)

path_gdf.explore(
    m=m,
    color="red", 
    tiles="CartoDB positron", 
    name="Route"
)


keyPoints = all_points[100:205]
geometry = [Point(xy) for xy in keyPoints]
gdf = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:26917")

# 3. Transform to WGS84 (EPSG:4326)
# This automatically handles the conversion for every point in the dataframe
gdf_wgs84 = gdf.to_crs(epsg=4326)

feature_group = folium.FeatureGroup(name="UTM Zone 17 Points")

# 6. Add points from GeoDataFrame to the FeatureGroup
for point in gdf_wgs84.geometry:
    folium.CircleMarker([point.y, point.x]).add_to(feature_group)

feature_group.add_to(m)
folium.LayerControl().add_to(m)

# Create a group for all points
# points_layer = folium.FeatureGroup(name="My Points")

# for point in all_points:
#     folium.CircleMarker(
#         location=[point[0], point[1]],
#         radius=5,
#         color='blue',
#         fill=True
#     ).add_to(points_layer)

# # Add the group to the map
# points_layer.add_to(m)


output = st_folium(m, width=700, height=500)

if output["last_clicked"]:
    lat = output["last_clicked"]["lat"]
    lng = output["last_clicked"]["lng"]

    click_gdf = gpd.GeoDataFrame(
        geometry=[Point(lat, lng)], crs="EPSG:4326"
    )

    projected_coord = click_gdf.to_crs("EPSG:26917")
    projected_x = projected_coord.geometry.x[0]
    projected_y = projected_coord.geometry.y[0]
    
    st.write("You clicked at: ", projected_x, projected_y)

# 4. Display the map in Streamlit
#import streamlit.components.v1 as components
#components.html(m._repr_html_(), height=500)

