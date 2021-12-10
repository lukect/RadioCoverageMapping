from pathlib import Path

# Project Root
ROOT_DIRECTORY = Path(__file__).parent.parent.resolve().__str__()

# Original elevation data
ORIGINAL_ELEVATION_DATA = ROOT_DIRECTORY + "/data/eu_dem_v11_E30N30.TIF"

# Cropped elevation data
CROPPED_ELEVATION_DATA = ROOT_DIRECTORY + "/data/Oban_cropped.TIF"

# Reprojected elevation data
REPROJECTED_ELEVATION_DATA = ROOT_DIRECTORY + "/data/Oban_reprojected.TIF"

# PROJECT_CRS = "EPSG:3035"
PROJECT_CRS = "EPSG:3857"
