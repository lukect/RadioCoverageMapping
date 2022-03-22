import numpy as np
from PIL import Image
from tqdm import tqdm

import defintions as defs
from terrain_map import TerrainMap
from terrain_map import load_map
from terrain_map.load_map import range_inclusive


def draw_red(map_img: np.ndarray, y: int, x: int, opacity: float):
    transparency = 1 - opacity
    map_img[y, x, 0] = round((map_img[y, x, 0] * transparency) + (255 * opacity))
    map_img[y, x, 1] = round((map_img[y, x, 1] * transparency) + (0 * opacity))
    map_img[y, x, 2] = round((map_img[y, x, 2] * transparency) + (0 * opacity))


def draw_deep_pink(map_img: np.ndarray, y: int, x: int):
    map_img[y, x, 0] = 255
    map_img[y, x, 1] = 20
    map_img[y, x, 2] = 147


def draw_yellow(map_img: np.ndarray, y: int, x: int):
    map_img[y, x, 0] = 255
    map_img[y, x, 1] = 255
    map_img[y, x, 2] = 0


def is_drawn(map_img: np.ndarray, y: int, x: int) -> bool:
    return map_img[y, x, 0] != 0 or map_img[y, x, 1] != 0 or map_img[y, x, 2] != 0


def draw_road_point(tm: TerrainMap, map_img: np.ndarray, y: int, x: int):
    for yy in range_inclusive(y - 1, y + 1):
        for xx in range_inclusive(x - 1, x + 1):
            if tm.exists((yy, xx)):
                draw_yellow(map_img, yy, xx)


def render(tm: TerrainMap, draw_roads: bool = True) -> np.ndarray:
    print("Searching for minimum and maximum elevation", flush=True)
    height_min = float("inf")
    height_max = float("-inf")
    max_loc = (-1, -1)
    min_loc = (-1, -1)
    yx_size = tm.shape()
    for y in range(yx_size[0]):
        for x in range(yx_size[1]):
            map_point = tm[y][x]
            if map_point.elevation > height_max and not map_point.water:
                height_max = map_point.elevation
                max_loc = (y, x)
            elif map_point.elevation < height_min and not map_point.water:
                height_min = map_point.elevation
                min_loc = (y, x)
    height_diff = height_max - height_min
    print("Min elv. = " + str(height_min) + "m @" + str(min_loc) + " | Max elv. = " + str(height_max) +
          "m @" + str(max_loc) + " | Diff elv. = " + str(height_diff) + "m", flush=True)

    print("Creating empty image rendering array", flush=True)
    # Create empty RGB image/pixel/map array
    map_render = np.zeros((yx_size[0], yx_size[1], 3), 'uint8')

    print("Render drawing started", flush=True)
    with tqdm(total=yx_size[0] * yx_size[1], smoothing=.025) as progress_bar:
        for y in range(0, yx_size[0]):
            for x in range(0, yx_size[1]):
                point = tm[y][x]
                if is_drawn(map_render, y,
                            x):  # Skip if already drawn on (if road [drawn as 3×3] is next to pixel)
                    continue
                elif draw_roads and point.road is True:
                    draw_road_point(tm, map_render, y, x)  # Draw road
                elif point.water is True:  # Draw water
                    map_render[y, x, 2] = 255  # Blue (band 2) for water
                else:  # Draw terrain
                    # Closest to min.height = 50G, closest to max.height = 200G | Green (band 1) for terrain
                    map_render[y, x, 1] = 50 + (((point.elevation - height_min) / height_diff) * 150)
                progress_bar.update(1)
    print("Finished drawing", flush=True)

    return map_render


def view(image: Image = None):
    if image is None:
        if load_map.loaded_terrain_map is None:
            load_map.generate()

        image = Image.fromarray(render(tm=load_map.loaded_terrain_map), mode="RGB")

    image.show(title="View Elevation Data")
    return image


def save(file_name: str = "map_with_roads.png", image: Image = None):
    if image is None:
        if load_map.loaded_terrain_map is None:
            load_map.generate()

        image = Image.fromarray(render(tm=load_map.loaded_terrain_map), mode="RGB")

    file_path = defs.OUTPUT_DIRECTORY / file_name
    print("Saving image to: " + str(file_path))
    image.save(fp=file_path, format="PNG", optimize=True)
    return image


if __name__ == "__main__":
    img = view()
    save(image=img)
