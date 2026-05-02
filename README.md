# campus-router-utm

An accessibility-focused routing engine for the University of Toronto Mississauga (UTM) campus. This tool enables users to generate paths that prioritize or avoid specific terrain types and slopes, ensuring a more navigable campus experience for everyone.

# Key Features
- Comprehensive Campus Mapping: Covers all major outdoor paths and primary indoor routes on the first floors of campus buildings.
- Customizable Routing Profiles: Adjust preferences for terrain types and elevation gain to suit individual mobility needs.
- Flexible Navigation: Search for specific destinations or manually select coordinates directly from the interactive map.
- Rich Visual Feedback:
  - Layer Toggles: Turn specific map features on or off for a cleaner view.
  - Interactive Markers: Click on notable points of interest to view names and details.
  - Path Data Overlays: Hover over suggested routes to see specific data points, such as exact slope percentages.
  - Color-Coded Terrain: Paths are visually categorized by surface type for quick identification.


# Data Sources
- Path Geometry: Sourced from OpenStreetMap (OSM).
- Elevation Data: Generated using LiDAR data and high-resolution DEM files obtained via the City of Mississauga’s open data portal.

# Installation
Prerequisites
- Python 3.8 or higher
- Git

Clone the repository:

```
git clone https://github.com/your-username/campus-router-utm.git
cd campus-router-utm
```

Set up the environment:

```
python -m venv env
source env/bin/activate  # On Windows use: env\Scripts\activate
```

Install dependencies:
```
pip install -r requirements.txt
```

# Usage

To launch the interactive dashboard locally, run:
```
streamlit run main.py
```

The application will be available in your browser at http://localhost:8501. It is also live at https://campus-router-utm-buacuzsj4vwdjyhpkt5jeg.streamlit.app/.

# Project Structure
```
campus-router-utm/
├── data/              # Geospatial datasets 
├── env/               # Local virtual environment (ignored by git)
├── main.py            # Main Streamlit application entry point
├── constants.py       # Configuration variables and terrain weights
├── requirements.txt   # Project dependencies
└── README.md          # Project documentation
```

# Project Shortcomings & Constraints

- Data Accuracy: Terrain types and Digital Elevation Model (DEM) data are subject to the precision of the source sets; indoor elevation data may have minor inaccuracies.

- Limited Multi Floor Scope: While a proof-of-concept exists for multi floor navigation exists in the form of the second floor library, other upper floors are omitted due to security considerations and data limitatations.

- Path Detail: Indoor data focuses on primary paths rather than granular room-to-room navigation.


# License
Licensed under the MIT License.
