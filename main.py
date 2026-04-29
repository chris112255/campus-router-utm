import pandas as pd
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString, Point
import streamlit as st
from streamlit_folium import st_folium
import folium

# TODO: Label all the points that are important in ArcGIS
# TODO: Add multifloors for IB
# TODO: USE A DESIGNATED POINTS FILE, show details on points like name
# TODO: MAKE A CONSTANTS FILE

# take in a list of points as a path and project them to WGSS84 for rendering
def get_map_data(path_coords):
    line = LineString(path_coords)
    gdf = gpd.GeoDataFrame(geometry=[line], crs="EPSG:26917")
    return gdf.to_crs(epsg=4326)

# custom weighting function for search
def calculate_weight(start, end, edge_data):
    # TODO: add a penalties map during before calling this and saving it into state to use here

    multiplier = 1
    p = st.session_state.preferences
    e = edge_data

    if p["avoid_heavy_slope"]: 
        # if slope_max > 12:
        #     multiplier *= 100
        # elif slope_max > 5:
        #     multiplier *= (slope_max - 5) / 10 + 1
        pass

    if p["avoid_gravel"] or p["avoid_asphalt"] or p["avoid_dirt"] or p["avoid_unpaved"]:
        multiplier *= 1.5

    if p["avoid_parking"]:
        multiplier *= 1.5

    if p["avoid_indoors"]:
        multiplier *= 1.25

    if p["prioritize_paved"] or p["prioritize_ground"] or p["prioritize_indoors"] or p["prioritize_concrete"] or p["prioritize_sidewalk"]:
        multiplier *= 0.75

    if p["prioritize_crosswalk"]:
        multiplier = 0.01

    if p["prioritize_easy_path"]:
        multiplier *= edge_data.get('avg_slope') / 100 + 1

    weighted_total = edge_data.get('length') * multiplier
    return weighted_total

# reset state on routing mode change
def reset_state():
    st.session_state.drop_start = False
    st.session_state.drop_dest = False
    st.session_state.start_coord = False
    st.session_state.dest_coord = False

# intialize state
def initialize_state():
    if "graph" not in st.session_state:
        st.session_state.graph = None
    if "gdf" not in st.session_state:
        st.session_state.gdf = None
    if "gdf_wgs84" not in st.session_state:
        st.session_state.gdf_wgs84 = None
    if "drop_start" not in st.session_state:
        st.session_state.drop_start = False
    if "drop_dest" not in st.session_state:
        st.session_state.drop_dest = False
    if "start_coord" not in st.session_state:
        st.session_state.start_coord = False
    if "dest_coord" not in st.session_state:
        st.session_state.dest_coord = False
    if "recalculate" not in st.session_state:
        st.session_state.recalculate = False    
    if "routing_preferences" not in st.session_state:
        st.session_state.preferences = {   
            "avoid_heavy_slope": False,
            "avoid_gravel": False,
            "avoid_asphalt": False,
            "avoid_dirt": False,
            "avoid_unpaved": False,
            "avoid_parking": False,
            "avoid_indoors": False,
            "prioritize_paved": False,
            "prioritize_ground": False,
            "prioritize_indoors": False,
            "prioritize_concrete": False,
            "prioritize_sidewalk": False,
            "prioritize_crosswalk": False,
            "prioritize_easy_path": False,
        }

# handle map clicking 
def handle_click(map_data, gdf):
    if (map_data["last_clicked"] and 
        (st.session_state.drop_start or st.session_state.drop_dest)):
        lat = map_data["last_clicked"]["lat"]
        lng = map_data["last_clicked"]["lng"]

        # create a 100m buffer around point
        point_clicked_wgs = gpd.GeoSeries([Point(lng, lat)], crs="EPSG:4236")
        point_clicked_utm = point_clicked_wgs.to_crs("EPSG:26917")
        click_buffered = point_clicked_utm.buffer(100)
        buffered_gdf = gpd.GeoDataFrame(geometry=click_buffered)

        # find points in the buffer
        nearby_points = gpd.sjoin(gdf, buffered_gdf, how="inner", predicate="intersects")

        if map_data and map_data.get("bounds"):
            st.session_state.map_bounds = map_data["bounds"]
            st.session_state.map_zoom = map_data["zoom"]

        # find the nearest point and snap to it
        def drop_and_snap(trigger_key, coord_key):
            if st.session_state[trigger_key]:
                st.session_state[trigger_key] = False

                if not nearby_points.empty:
                    distances = nearby_points.geometry.distance(point_clicked_utm.iloc[0])
                    nearest_idx = distances.idxmin()
                    
                    st.session_state[coord_key] = nearest_idx
                    st.rerun()
                else:
                    st.toast("Point out of range", icon="❌")

        # do this for both start and end
        drop_and_snap("drop_start", "start_coord")
        drop_and_snap("drop_dest", "dest_coord")

def display_routing_ui(locations):
    mode = st.radio("Point Selection", ["Search", "Map"], on_change=reset_state)

    # search routing UI
    if mode == "Search":            
        def update_marker_start():
            st.session_state.start_coord = locations.get(st.session_state.key_start)
        def update_marker_dest():
            st.session_state.dest_coord = locations.get(st.session_state.key_end)

        col1, col2 = st.columns(2)
        with col1:
            start_selection = st.selectbox(
                "Choose Start:", 
                options=locations.keys(),
                placeholder="Start typing to search...",
                index=None,
                key="key_start",
                on_change=update_marker_start
            )
        with col2:
            end_selection = st.selectbox(
                "Choose Destination:", 
                options=locations.keys(),
                placeholder="Start typing to search...",
                index=None,
                key="key_end",
                on_change=update_marker_dest
            )

    # map picking routing UI
    else:
        col1, col2 = st.columns(2)
        with col1:
            drop_start = st.button("Pick Start")
            if drop_start:
                st.session_state.drop_start = True
                st.session_state.drop_dest = False
                st.session_state.start_coord = None
                st.rerun()
        with col2:
            drop_dest = st.button("Pick End")
            if drop_dest:
                st.session_state.drop_dest = True
                st.session_state.drop_start = False    
                st.session_state.dest_coord = None
                st.rerun()

def display_additional_options_ui():
    with st.expander("Show Routing Preferences", expanded=False):
        st.write("Avoid: ")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.checkbox("Gravel", key="gravel")
            st.checkbox("Asphalt", key="asphalt")
        with col2:
            st.checkbox("Dirt", key="dirt")
            st.checkbox("Unpaved", key="unpaved")
        with col3:
            st.checkbox("Indoors", key="avoid_indoors")
            st.checkbox("Heavy Slopes", key="heavy_slope")
        with col4:
            st.checkbox("Parking", key="parking")

        st.write("Prioritize: ")
        col5, col6, col7, col8 = st.columns(4)
        with col5:
            st.checkbox("Easy Paths", key="easy_path")
            st.checkbox("Indoors", key="prio_indoors")
        with col6:
            st.checkbox("Paved", key="paved")
            st.checkbox("Ground", key="ground")
        with col7:        
            st.checkbox("Concrete", key="concrete")
            st.checkbox("Sidewalks", key="sidewalk")
        with col8:
            st.checkbox("Crosswalks", key="crosswalk")

        if st.button("Apply Advanced Settings"):
            s = st.session_state
            p = s.preferences
            
            p["avoid_gravel"] = s.gravel
            p["avoid_heavy_slope"] = s.heavy_slope
            p["avoid_asphalt"] = s.asphalt
            p["avoid_dirt"] = s.dirt
            p["avoid_unpaved"] = s.unpaved
            p["avoid_parking"] = s.parking
            p["avoid_indoors"] = s.avoid_indoors

            p["prioritize_paved"] = s.paved
            p["prioritize_ground"] = s.ground
            p["prioritize_indoors"] = s.prio_indoors
            p["prioritize_concrete"] = s.concrete
            p["prioritize_sidewalk"] = s.sidewalk
            p["prioritize_crosswalk"] = s.crosswalk
            p["prioritize_easy_path"] = s.easy_path

            st.session_state.recalculate = True
            st.rerun()

def display_start_end_markers(m, gdf_wgs84):
    # draw a marker if a start or dest was selected
    if st.session_state.start_coord:
        wgs_location = gdf_wgs84.loc[st.session_state.start_coord].geometry

        startMarker = folium.Marker(
            location=[wgs_location.y, wgs_location.x],
            icon=folium.Icon(color="green", icon="info-sign"),
            tooltip="Start",
        ).add_to(m)    

    if st.session_state.dest_coord:
        print("draw dest")
        wgs_location = gdf_wgs84.loc[st.session_state.dest_coord].geometry

        endMarker = folium.Marker(
            location=[wgs_location.y, wgs_location.x],
            icon=folium.Icon(color="red", icon="info-sign"),
            tooltip="End",
        ).add_to(m)    

def display_path(G, m, gdf):
    # render path if a start and end have been selected and theyre not the same
    if st.session_state.start_coord and st.session_state.dest_coord and st.session_state.start_coord != st.session_state.dest_coord: 
        # get start and dest
        if st.session_state.start_coord:
            utm_location = gdf.loc[st.session_state.start_coord].geometry
            start_node=(utm_location.x, utm_location.y, utm_location.z)
        if st.session_state.dest_coord:
            utm_location = gdf.loc[st.session_state.dest_coord].geometry
            end_node=(utm_location.x, utm_location.y, utm_location.z)

        # find shortest path and render it
        shortest_path = nx.shortest_path(G, start_node, end_node, weight=calculate_weight)
        path_gdf = get_map_data(shortest_path)
        path_gdf.explore(
            m=m,
            color="red", 
        )

def display_searchable_markers(m, gdf_wgs84, locations):
    # add markers for searchable areas
    feature_group = folium.FeatureGroup(name="Notable Areas")

    for value in locations.values():
        point = gdf_wgs84.geometry.get(value)
        folium.Marker([point.y, point.x], popup=f"X: {point.x}", icon=folium.Icon(color="blue", icon="info-sign")).add_to(feature_group)

    feature_group.add_to(m)

def build_graph():
    df = pd.read_csv('paths.csv')
    G = nx.Graph()
    all_points = []

    for index, row in df.iterrows():
        all_points.append((row.start_x, row.start_y, row.start_z))

        start = (row.start_x, row.start_y, row.start_z)
        end = (row.end_x, row.end_y, row.end_z)
        
        G.add_edge(start, end, name=row.name, avg_slope=row.slope_avg, length=row.length)
    return G, all_points

def create_gdfs(all_points):
    # create list of points from all points and turn it into a gdf
    geometry = [Point(xyz) for xyz in all_points]
    gdf = gpd.GeoDataFrame(geometry=geometry, crs="EPSG:26917")

    # make a copy with WGS84 coords
    gdf_wgs84 = gdf.to_crs(epsg=4326)
    return gdf, gdf_wgs84

@st.cache_data
def get_processed_data():
    G, all_points = build_graph()
    gdf, gdf_wgs84 = create_gdfs(all_points)
    return G, gdf, gdf_wgs84

def main():
    # searchable locations
    locations = {
        "William G Davis Building": 1, 
        "Instructional Centre": 10,
        "Deerfield Hall": 13
        }

    initialize_state()

    # intitalize data and populate graph
    G, gdf, gdf_wgs84 = get_processed_data()
    
    # render map
    st.title("UTM Route Mapper")
    center = [43.5494114, -79.6637835]

    m = folium.Map(location=center, zoom_start=16)

    if st.session_state.recalculate:
        st.session_state.recalculate = False
        st.toast("Settings applied!")

    display_routing_ui(locations)
    display_additional_options_ui()
    display_searchable_markers(m, gdf_wgs84, locations)
    display_start_end_markers(m, gdf_wgs84)
    display_path(G, m, gdf)

    # add ability to toggle layers
    folium.LayerControl().add_to(m)

    # display map
    map_data = st_folium(m, width=700, height=500)

    # handle adding start/dest
    handle_click(map_data, gdf)

main()