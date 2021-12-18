from pathlib import Path

# Project Root
ROOT_DIRECTORY = Path(__file__).parent.parent.resolve()
DATA_DIRECTORY = ROOT_DIRECTORY / "data"

# Original elevation data
ORIGINAL_ELEVATION_DATA = DATA_DIRECTORY / "eu_dem_v11_E30N30.TIF"

# Reprojected elevation data
REPROJECTED_ELEVATION_DATA = DATA_DIRECTORY / "Oban_REPROJECTED.TIF"

# FINAL (cropped) elevation data
FINAL_ELEVATION_DATA = DATA_DIRECTORY / "Oban_FINAL.TIF"

# PROJECT_CRS = "EPSG:3035"
PROJECT_CRS = "EPSG:3857"
