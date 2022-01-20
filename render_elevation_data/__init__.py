import numpy as np
import rasterio
from PIL import Image

import defintions as defs


def render(elevation_data):
    with rasterio.open(elevation_data) as src:
        print("Rendering Elevation Data")
        data_band = src.read(1)
        print("Elevation Data Shape = " + str(data_band.shape))
        height_min = float("inf")
        height_max = float("-inf")
        for y in data_band:
            for x in y:
                if x > height_max and x != defs.EU_DEM_SEA_LEVEL:
                    height_max = x
                if x < height_min and x != defs.EU_DEM_SEA_LEVEL:
                    height_min = x
        height_diff = height_max - height_min
        print("Min = " + str(height_min) + " | Max = " + str(height_max) + " | Diff = " + str(height_diff))

        # Create empty RGB image/pixel/map array
        height_map = np.zeros((data_band.shape[0], data_band.shape[1], 3), 'uint8')

        # Render map | Need Y,X because the EU-DEM data is in Y,X not X,Y
        for y in range(0, data_band.shape[0]):
            for x in range(0, data_band.shape[1]):
                if data_band[y][x] == defs.EU_DEM_SEA_LEVEL:  # Draw water
                    height_map[y, x, 2] = 255  # Blue (band 2) for water
                else:  # Draw terrain
                    # Closest to min.height = 50G, closest to max.height = 200G | Green (band 1) for terrain
                    height_map[y, x, 1] = 50 + (((data_band[y][x] - height_min) / height_diff) * 150)

        return height_map


def view(rendered_map=None):
    if rendered_map is None:
        rendered_map = render(defs.FINAL_ELEVATION_DATA)

    img = Image.fromarray(rendered_map, mode="RGB")
    img.show(title="View Elevation Data")


def save(rendered_map=None, file_name="map.png"):
    if rendered_map is None:
        rendered_map = render(defs.FINAL_ELEVATION_DATA)

    img = Image.fromarray(rendered_map, mode="RGB")
    img.save(fp=defs.OUTPUT_DIRECTORY / file_name, format="PNG", optimize=True)


if __name__ == "__main__":
    render = render(defs.FINAL_ELEVATION_DATA)
    view(render)
    save(render)
