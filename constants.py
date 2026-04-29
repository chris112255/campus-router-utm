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