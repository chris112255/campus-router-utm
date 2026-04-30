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
    "William G Davis Building Entrance 1": 7137, 
    "William G Davis Building Entrance 2": 6619, 
    "William G Davis Building Entrance 3": 6524, 
    "Instructional Centre Entrance 1": 6586,
    "Instructional Centre Entrance 2": 7065,
    "Instructional Centre Entrance 3": 5952,
    "Instructional Centre Entrance 4": 5378,
    "Maangiwe Nendowamin Entrance 1": 6846,
    "Maangiwe Nendowamin Entrance 2": 5408,
    "Maangiwe Nendowamin Entrance 3": 6854,
    "Culture, Communications, Technology Entrance 1": 6544,
    "Culture, Communications, Technology Entrance 2": 6600,
    "Putnam Residence": 313,
    "McGrath Valley Residence": 540,
    "UTM Alumni House": 674,
    "Oscar Peterson House Entrance 1": 1008,
    "Oscar Peterson Hall Entrance 2": 7251,
    "Roy Ivor Hall Residence": 1230, 
    "Deerfield Hall Entrance 1": 1396,
    "Deerfield Hall Entrance 2": 5838,
    "McLuhan Court Residence": 1461,
    "Bus Stop": 1562,
    "Parking Lot 1": 2900,
    "Engineering and Grounds Building": 2983,

    "UTM Nature Trail Entrance 1": 3794,
    "UTM Nature Trail Entrance 2": 4166,
    "Library": 7556,

    "UTM Grounds Building": 6707,
    "Schreiberwood Residence": 1432, 
    "Parking Lot 7": 3148,
    "Parking Lot 8": 4410,
    "Parking Lot 9": 4968,
    "Gym A/B": 7676,
    "Gym C": 7674,
    "Science Building Entrance 1": 7316,
    "Science Building Entrance 2": 7615,
    "Starbucks": 7553, 
    "Erindale Studio Theatre": 7504,
    "Erindale Hall": 7496,
    "Parking Lot 10": 7404,
    "The Blink Duck": 7376,
    "Student Centre": 7277,
    "Lealock Lane": 5310,
    "Kaneff Entrance 1": 7197,
    "Kaneff Entrance 2": 6626,
    "Kaneff Entrance 3": 1060,
    "Kaneff Entrance 4": 7191,
    "Recreation, Athletics, and Wellness Centre": 7180,
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