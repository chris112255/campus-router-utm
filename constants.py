# coordinate systems
UTM17 = "26917"
WGS = "4326"

# weighting related
UNKNOWN_MULT = 1.1
HEAVY_SLOPE = 11
HEAVY_SLOPE_MULT = 11
MODERATE_SLOPE = 5

# surface penalties
GRAVEL = 1.5
ASPHALT = 1.5
DIRT = 1.5
UNPAVED = 1.5
PARKING = 1.5
AVOID_INDOOR = 1.25
PAVED = 0.75
GROUND = 0.75
INDOOR = 0.75
CONCRETE = 0.75
SIDEWALK = 0.75
CROSSING = 0.01

# etc
SNAP_BUFFER = 100

# files
PATHS = "paths.csv"
POINTS = "points.csv"

# searchable locations
LOCATIONS = {
    "William G Davis Building": 1, 
    "Instructional Centre": 10,
    "Deerfield Hall": 13
}

# map settings
MAP_CENTER = [43.5494114, -79.6637835]
ZOOM_START = 16
WIDTH = 700
HEIGHT = 500
PATH_WEIGHT = 7

SURFACE_COLOURS = {
    "crossing": "#00FFFF",
    "sidewalk": "#228B22",
    "concrete": "#FF8C00",
    "paved": "#4682B4",
    "indoor": "#DAA520",
    "ground": "#FFD700",
    "asphalt": "#2F4F4F",
    "gravel": "#A52A2A",
    "dirt": "#8B4513",
    "unpaved": "#D2691E",
    "parking": "#800080",
    "unknown": "#FF0000" # Use Bright Red for your empty Excel cells!
}