import pandas as pd
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString
import streamlit as st

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

all_x_vals = []
all_y_vals = []

for index, row in df.iterrows():
    all_x_vals.append(row.start_x)
    all_y_vals.append(row.start_y)

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
m = path_gdf.explore(
    color="red", 
    tiles="CartoDB positron", 
    name="Route"
)

# 4. Display the map in Streamlit
import streamlit.components.v1 as components
components.html(m._repr_html_(), height=500)

