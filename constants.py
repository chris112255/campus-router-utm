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
    "William G Davis Building": {"index": 7136, "importance": "high"},
    "Instructional Centre": {"index": 6585, "importance": "high"},
    "Maangiwe Nendowamin": {"index": 6845, "importance": "high"},
    "Culture, Communications & Technology Building": {"index": 6543, "importance": "high"},
    "Putnam Residence": {"index": 311, "importance": "low"},
    "McGrath Valley Residence": {"index": 539, "importance": "low"},
    "UTM Alumni House": {"index": 673, "importance": "low"},
    "Oscar Peterson Hall": {"index": 7250, "importance": "low"},
    "Roy Ivor Hall Residence": {"index": 1229, "importance": "low"},
    "Deerfield Hall": {"index": 1395, "importance": "high"},
    "McLuhan Court Residence": {"index": 1460, "importance": "low"},
    "Bus Stop": {"index": 1561, "importance": "low"},
    "Parking Lot 1": {"index": 2899, "importance": "low"},
    "Engineering and Grounds Building": {"index": 2982, "importance": "low"},
    "UTM Nature Trail": {"index": 4165, "importance": "low"},
    "Library": {"index": 7555, "importance": "low"},
    "UTM Grounds Building": {"index": 6706, "importance": "low"},
    "Schreiberwood Residence": {"index": 1431, "importance": "low"},
    "Parking Lot 7": {"index": 3147, "importance": "low"},
    "Parking Lot 8": {"index": 4409, "importance": "low"},
    "Parking Lot 9": {"index": 4967, "importance": "low"},
    "Gym A/B": {"index": 7675, "importance": "low"},
    "Gym C": {"index": 7673, "importance": "low"},
    "Health Science Complex": {"index": 7614, "importance": "low"},
    "Starbucks": {"index": 7552, "importance": "low"},
    "Erindale Studio Theatre": {"index": 7503, "importance": "low"},
    "Erindale Hall": {"index": 7495, "importance": "low"},
    "Parking Lot 10": {"index": 7404, "importance": "low"},
    "The Blink Duck": {"index": 7375, "importance": "low"},
    "Student Centre": {"index": 7276, "importance": "low"},
    "Lealock Lane": {"index": 5309, "importance": "low"},
    "Kaneff Centre": {"index": 6625, "importance": "high"},
    "Recreation, Athletics, and Wellness Centre": {"index": 7179, "importance": "low"},
    "Science Building": {"index": 6523, "importance": "high"},
    "Library Floor 2": {"index": 7717, "importance": "low"}
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
    "unknown": "#FF0000"
}