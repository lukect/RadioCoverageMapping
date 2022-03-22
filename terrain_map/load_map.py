import math

import osmnx
import rasterio
from tqdm import tqdm

import defintions as defs
import defintions.Coordinates as Coords
from terrain_map import *


def range_inclusive(start: int, end: int):
    return range(start, end + 1)


def get_road_map_points(tmap: TerrainMap, coords_list: List[Tuple[float, float]]) -> List[Tuple[int, int]]:
    map_points: List[Tuple[int, int]] = []

    for coords in coords_list:
        raw_map_point = tmap.coords_to_map_yx(coords)
        if len(map_points) > 0:
            last_point = map_points[-1]
            diff_y = raw_map_point[0] - last_point[0]
            diff_x = raw_map_point[1] - last_point[1]
            dist = math.sqrt(diff_y ** 2 + diff_x ** 2)
            dist_int = int(dist)
            for n in range(1, dist_int):
                waypoint = (int(last_point[0] + ((diff_y / dist_int) * n)),
                            int(last_point[1] + ((diff_x / dist_int) * n)))
                if waypoint not in map_points and tmap.exists(waypoint):
                    map_points.append(waypoint)
        if tmap.exists(raw_map_point):
            map_points.append(raw_map_point)

    return map_points


loaded_terrain_map: TerrainMap | None = None


def generate(elevation_data=defs.FINAL_ELEVATION_DATA):
    # Elevation Data
    with rasterio.open(elevation_data) as src:
        print("Loading Elevation Data", flush=True)
        transform = src.transform
        transformer = Transformer.from_crs(crs_from=Coords.crs, crs_to=src.crs, always_xy=True)
        data_band = src.read(1)
        assert data_band.shape[0] > 0 and data_band.shape[1] > 0
        print("Creating an empty TerrainMap", flush=True)
        tm = create_empty_TerrainMap(data_band.shape[0], data_band.shape[1], transformer, transform)
        print("Created an empty TerrainMap with shape (y, x) = " + str(tm.shape()), flush=True)

        print("Filling TerrainMap with Elevation & Water Data", flush=True)
        with tqdm(total=data_band.shape[0] * data_band.shape[1], smoothing=.025) as progress_bar:
            for y in range(0, data_band.shape[0]):
                for x in range(0, data_band.shape[1]):
                    if data_band[y][x] == defs.EU_DEM_SEA_LEVEL:
                        tm[y][x].water = True
                    else:
                        tm[y][x].elevation = data_band[y][x]
                    progress_bar.update(1)
        print("Finished loading Elevation & Water Data", flush=True)

    # Road Data
    print("Loading Road Data", flush=True)
    road_data = osmnx.graph_from_bbox(west=Coords.nw_corner[0], north=Coords.nw_corner[1], east=Coords.se_corner[0],
                                      south=Coords.se_corner[1], network_type='drive', retain_all=True,
                                      truncate_by_edge=True, clean_periphery=True)

    print("Filling TerrainMap with Road Data", flush=True)
    for road in road_data.edges(data=True):
        if "geometry" in road[2]:
            geo_points = road[2]["geometry"]
            for map_point in get_road_map_points(tm, geo_points.coords):
                y = map_point[0]
                x = map_point[1]
                tm[y][x].road = True

    global loaded_terrain_map
    loaded_terrain_map = tm

    print("Finished generating TerrainMap", flush=True)
    return tm


if __name__ == "__main__":
    generate(elevation_data=defs.FINAL_ELEVATION_DATA)
    print("TerrainMap successfully loaded", flush=True)
