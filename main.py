import pandas as pd
import networkx as nx
import geopandas as gpd
from shapely.geometry import LineString, Point
import streamlit as st
from streamlit_folium import st_folium
import folium
import constants as c
from typing import List, Any, Tuple, Dict, Optional

s = st.session_state

# change page size and heading style
def set_content_size() -> None:
    st.markdown(
        """
        <style>
        .stMainBlockContainer {
            max-width: """ + c.MAX_WIDTH + """;
            width:""" + c.PAGE_WIDTH + """!important;
            min-width: """ + c.MIN_WIDTH + """;
        }
        .stMainBlockContainer h1 {margin: 0; padding: 0}
        </style>
        """,
        unsafe_allow_html=True,
    )

# take in a list of points as a path and project them to WGSS84 for rendering
def get_map_data(G: nx.Graph, path_nodes: List[Any]) -> gpd.GeoDataFrame:
    segments = []
    
    # loop through start and end labelling each
    for i in range(len(path_nodes) - 1):
        u = path_nodes[i]
        v = path_nodes[i+1]
        
        edge_data = G.get_edge_data(u, v)
        
        segments.append({
            'geometry': LineString([[u[0], u[1]], [v[0], v[1]]]),
            'surface': edge_data.get('surface'),
            "name": edge_data.get("name"),
            "slope": edge_data.get("avg_slope"),
            "colour": c.SURFACE_COLOURS.get(edge_data.get('surface'), "#000000"),
            "floor": edge_data.get("floor")
        })
    
    gdf = gpd.GeoDataFrame(segments, crs=f"EPSG:{c.UTM17}")
    return gdf.to_crs(epsg=c.WGS)

# custom weighting function for search
def calculate_weight(_start: Tuple[float, float, float], _end: Tuple[float, float, float], edge_data: Dict[str, Any]) -> float:
    p = s.preferences

    if edge_data.get("surface") == "unknown": multiplier = c.UNKNOWN_MULT
    else: multiplier = s.weighting_map.get(edge_data.get("surface"))

    if p["avoid_heavy_slope"]: 
        slope_max = edge_data.get("slope_max")

        if slope_max > c.HEAVY_SLOPE:
            multiplier = c.HEAVY_SLOPE_MULT
        elif slope_max > c.MODERATE_SLOPE:
            multiplier *= (slope_max - c.MODERATE_SLOPE) / 10 + 1

    if p["prioritize_easy_path"]:
        multiplier *= edge_data.get('avg_slope') / 100 + 1

    weighted_total = edge_data.get('length') * multiplier
    return weighted_total

# reset state on routing mode change
def reset_state() -> None:
    s.drop_start = False
    s.drop_dest = False
    s.start_coord = False
    s.dest_coord = False

# intialize state
def initialize_state() -> None:
    if "drop_start" not in s:
        s.drop_start = False
    if "drop_dest" not in s:
        s.drop_dest = False
    if "start_coord" not in s:
        s.start_coord = False
    if "dest_coord" not in s:
        s.dest_coord = False
    if "recalculate" not in s:
        s.recalculate = False    
    if "weighting_map" not in s:
        s.weighting_map = {
            "gravel": 1,
            "asphalt": 1,
            "dirt": 1,
            "unpaved": 1,
            "parking_aisle": 1,
            "indoor": 1,
            "paved": 1,
            "ground": 1,
            "indoor": 1,
            "concrete": 1,
            "sidewalk": 1,
            "crossing": 1
        }    
    if "preferences" not in s:
        s.preferences = {   
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
def handle_click(map_data: Dict[str, Any], gdf: gpd.GeoDataFrame) -> None:
    if (map_data["last_clicked"] and 
        (s.drop_start or s.drop_dest)):
        lat = map_data["last_clicked"]["lat"]
        lng = map_data["last_clicked"]["lng"]

        # create a 100m buffer around point
        point_clicked_wgs = gpd.GeoSeries([Point(lng, lat)], crs=f"EPSG:{c.WGS}")
        point_clicked_utm = point_clicked_wgs.to_crs(f"EPSG:{c.UTM17}")
        click_buffered = point_clicked_utm.buffer(c.SNAP_BUFFER)
        buffered_gdf = gpd.GeoDataFrame(geometry=click_buffered)

        # find points in the buffer
        nearby_points = gpd.sjoin(gdf, buffered_gdf, how="inner", predicate="intersects")

        if map_data and map_data.get("bounds"):
            s.map_bounds = map_data["bounds"]
            s.map_zoom = map_data["zoom"]

        # find the nearest point and snap to it
        def drop_and_snap(trigger_key: str, coord_key: str) -> None:
            if s[trigger_key]:
                s[trigger_key] = False

                if not nearby_points.empty:
                    distances = nearby_points.geometry.distance(point_clicked_utm.iloc[0])
                    nearest_idx = distances.idxmin()
                    
                    s[coord_key] = nearest_idx
                    st.rerun()
                else:
                    st.toast("Point out of range", icon="❌")

        # do this for both start and end
        drop_and_snap("drop_start", "start_coord")
        drop_and_snap("drop_dest", "dest_coord")

def display_routing_ui(locations: Dict[str, Dict[str, Any]]) -> None:
    mode = st.radio("Point Selection", ["Search", "Map"], on_change=reset_state)

    # search routing UI
    if mode == "Search":            
        def update_marker_start():
            if locations.get(s.key_start):
                s.start_coord = locations.get(s.key_start).get("index")
        def update_marker_dest():
            if locations.get(s.key_end):
                s.dest_coord = locations.get(s.key_end).get("index")

        start_selection = st.selectbox(
            "Choose Start:", 
            options=locations.keys(),
            placeholder="Start typing to search...",
            index=None,
            key="key_start",
            on_change=update_marker_start
        )
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
                s.drop_start = True
                s.drop_dest = False
                s.start_coord = None
                st.rerun()
        with col2:
            drop_dest = st.button("Pick End")
            if drop_dest:
                s.drop_dest = True
                s.drop_start = False    
                s.dest_coord = None
                st.rerun()

def display_additional_options_ui() -> None:
    with st.expander("Show Routing Preferences", expanded=False):
        st.write("Avoid: ")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.checkbox("Gravel", key="gravel")
            st.checkbox("Asphalt", key="asphalt")
            st.checkbox("Dirt", key="dirt")
        with col2:
            st.checkbox("Unpaved", key="unpaved")
            st.checkbox("Indoors", key="avoid_indoors")
        with col3:
            st.checkbox("Heavy Slopes", key="heavy_slope")
            st.checkbox("Parking", key="parking")

        st.write("Prioritize: ")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.checkbox("Easy Paths", key="easy_path")
            st.checkbox("Indoors", key="prio_indoors")
            st.checkbox("Crosswalks", key="crosswalk")
        with col2:
            st.checkbox("Ground", key="ground")
            st.checkbox("Sidewalks", key="sidewalk")
        with col3:
            st.checkbox("Concrete", key="concrete")
            st.checkbox("Paved", key="paved")

        if st.button("Apply Advanced Settings"):
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

            s.recalculate = True
            st.rerun()

def display_start_end_markers(m: folium.Map, gdf_wgs84: gpd.GeoDataFrame) -> None:
    # draw a marker if a start or dest was selected
    # should use an index for this instead ideally instead of saving a coord
    if s.start_coord:
        wgs_location = gdf_wgs84.loc[s.start_coord].geometry

        startMarker = folium.Marker(
            location=[wgs_location.y, wgs_location.x],
            icon=folium.Icon(color="green", icon="info-sign"),
            tooltip="Start",
        ).add_to(m)    

    if s.dest_coord:
        wgs_location = gdf_wgs84.loc[s.dest_coord].geometry

        endMarker = folium.Marker(
            location=[wgs_location.y, wgs_location.x],
            icon=folium.Icon(color="red", icon="info-sign"),
            tooltip="End",
        ).add_to(m)    

def calculate_best_path(G: nx.Graph, gdf: gpd.GeoDataFrame) -> Optional[List[Any]]:    
    # render path if a start and end have been selected and theyre not the same
    if s.start_coord and s.dest_coord and s.start_coord != s.dest_coord: 
        # get start and dest
        if s.start_coord:
            utm_location = gdf.loc[s.start_coord].geometry
            start_node=(utm_location.x, utm_location.y, utm_location.z)
        if s.dest_coord:
            utm_location = gdf.loc[s.dest_coord].geometry
            end_node=(utm_location.x, utm_location.y, utm_location.z)

        p = s.preferences
        w = s.weighting_map

        if p["avoid_gravel"] : w["gravel"] = c.GRAVEL
        if p["avoid_asphalt"] : w["asphalt"] = c.ASPHALT
        if p["avoid_dirt"] : w["dirt"] = c.DIRT
        if p["avoid_unpaved"]: w["unpaved"] = c.UNPAVED
        if p["avoid_parking"]: w["parking_aisle"] = c.PARKING
        if p["avoid_indoors"]: w["indoor"] = c.AVOID_INDOOR
        if p["prioritize_paved"]: w["paved"] = c.PAVED
        if p["prioritize_ground"]: w["ground"] = c.GROUND
        if p["prioritize_indoors"]: w["indoor"] = c.INDOOR
        if p["prioritize_concrete"]: w["concrete"] = c.CONCRETE
        if p["prioritize_sidewalk"]: w["sidewalk"] = c.SIDEWALK
        if p["prioritize_crosswalk"]: w["crossing"] = c.CROSSING
        
        shortest_path = nx.shortest_path(G, start_node, end_node, weight=calculate_weight)
        return shortest_path
    return None

# render path
def display_path(G: nx.Graph, path: List[Any], m: folium.Map) -> None:
    path_gdf = get_map_data(G, path)

    unique_floors = path_gdf['floor'].unique()
    unique_floors.sort()

    # render different floors separately
    for floor in unique_floors:
        fg = folium.FeatureGroup(name=f"Floor {floor}", show=True)
        
        floor_mask = path_gdf[path_gdf['floor'] == floor]
        floor_mask.explore(
            m=fg,
            tooltip=["name", "surface", "slope"],
            highlight=True,
            color=floor_mask["colour"], 
            style_kwds={'weight': c.PATH_WEIGHT}
        )
        fg.add_to(m)

def display_searchable_markers(m: folium.Map, gdf_wgs84: gpd.GeoDataFrame, locations: Dict[str, Dict[str, Any]]) -> None:
    # add markers for searchable areas
    feature_group = folium.FeatureGroup(name="Notable Areas")

    for v in locations.values():
        value = v.get("index")
        color = "blue"

        if v.get("importance") == "high":
            color = "orange"
        row = gdf_wgs84.loc[value]

        point = row.geometry
        name = row["name"]

        folium.Marker([point.y, point.x], popup=name, icon=folium.Icon(color=color, icon="info-sign")).add_to(feature_group)

    feature_group.add_to(m)

def build_graph() -> None:
    df = pd.read_csv(c.PATHS)
    G = nx.Graph()

    for index, row in df.iterrows():
        start = (row.start_x, row.start_y, row.start_z)
        end = (row.end_x, row.end_y, row.end_z)
        
        G.add_edge(start, end, name=row.edge_name, floor=row.floor, avg_slope=row.slope_avg, slope_max=row.slope_max, surface=row.surface, length=row.length)
    return G

def create_gdfs() -> None:
    all_points = pd.read_csv(c.POINTS)

    # create list of points from all points and turn it into a gdf
    gdf = gpd.GeoDataFrame(
        all_points[["name", "floor"]],
        geometry=gpd.points_from_xy(all_points["x"], all_points["y"], all_points["z"]), 
        crs=f"EPSG:{c.UTM17}"
    )

    # make a copy with WGS84 coords
    gdf_wgs84 = gdf.to_crs(epsg=c.WGS)
    return gdf, gdf_wgs84

# cache the graph and points gdfs
@st.cache_data
def get_processed_data() -> None:
    G = build_graph()
    gdf, gdf_wgs84 = create_gdfs()
    return G, gdf, gdf_wgs84

def main():
    set_content_size()
    initialize_state()

    # intitalize data and populate graph
    G, gdf, gdf_wgs84 = get_processed_data()
    
    m = folium.Map(location=c.MAP_CENTER, zoom_start=c.ZOOM_START)

    if s.recalculate:
        s.recalculate = False
        st.toast("Settings applied!")

    col1, col2 = st.columns([0.35, 0.65])

    with col1:
        st.title("UTM Route Mapper")
        display_routing_ui(c.LOCATIONS)
        display_additional_options_ui()

    display_searchable_markers(m, gdf_wgs84, c.LOCATIONS)
    display_start_end_markers(m, gdf_wgs84)
    path = calculate_best_path(G, gdf)
    if path:
        display_path(G, path, m)

    # add ability to toggle layers
    folium.LayerControl().add_to(m)

    with col2:
        map_data = st_folium(m, width=c.WIDTH)

    # handle adding start/dest
    handle_click(map_data, gdf)

if __name__ == "__main__":
    main()