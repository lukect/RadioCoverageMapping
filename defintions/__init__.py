from pathlib import Path

# Project Root
ROOT_DIRECTORY = Path(__file__).parent.parent.resolve()
DATA_DIRECTORY = ROOT_DIRECTORY / "data"
OUTPUT_DIRECTORY = ROOT_DIRECTORY / "output"

# Original elevation data
ORIGINAL_ELEVATION_DATA = DATA_DIRECTORY / "eu_dem_v11_E30N30.TIF"

# Reprojected elevation data
REPROJECTED_ELEVATION_DATA = DATA_DIRECTORY / "Oban_REPROJECTED.TIF"

# FINAL (cropped) elevation data
FINAL_ELEVATION_DATA = DATA_DIRECTORY / "Oban_FINAL.TIF"

# CRS used for processing in project (all data is converted to this before processing)
PROJECT_CRS = "EPSG:3857"

# Digital Elevation Model over Europe (EU-DEM) value to represent water in dataset
EU_DEM_SEA_LEVEL = -340282346638528859811704183484516925440  # (Negative of [FLOAT32 IEEE_754-1985 single MAX])
