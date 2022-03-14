import math

import osmnx
import rasterio
from affine import Affine
from pyproj import Transformer

import defintions as defs
import defintions.Coordinates as Coords
from terrain_map import *


def range_inclusive(start: int, end: int):
    return range(start, end + 1)


def get_map_points(coords_list: List[Tuple[float, float]], transformer: Transformer, affine_transform: Affine):
    map_points = []

    for coords in coords_list:
        raw_map_point = ~affine_transform * transformer.transform(coords[0], coords[1])
        raw_map_point = tuple(map(int, raw_map_point))

        if len(map_points) > 0:
            last_point = map_points[-1]
            diff_x = raw_map_point[0] - last_point[0]
            diff_y = raw_map_point[1] - last_point[1]
            dist = math.sqrt(diff_x ** 2 + diff_y ** 2)
            dist_int = int(dist)
            for n in range(1, int(dist)):
                midpoint = (int(last_point[0] + ((diff_x / dist_int) * n)),
                            int(last_point[1] + ((diff_y / dist_int) * n)))
                if midpoint not in map_points:
                    map_points.append(midpoint)
        map_points.append(raw_map_point)

    return map_points


loaded_terrain_map: TerrainMap | None = None


def load(elevation_data=defs.FINAL_ELEVATION_DATA):
    tm = None
    crs = None
    transform = None

    # Elevation Data
    with rasterio.open(elevation_data) as src:
        print("Loading Elevation Data")
        crs = src.crs
        transform = src.transform
        data_band = src.read(1)
        print("Creating an empty TerrainMap")
        # For some reason shape is x-y, although data is y-x
        tm = create_empty_TerrainMap(data_band.shape[1], data_band.shape[0])
        print("Created an empty TerrainMap with shape (y, x) = " + str(tm.shape()))

        print("Filling TerrainMap with Elevation & Water Data")
        for y in range(0, data_band.shape[0]):
            for x in range(0, data_band.shape[1]):
                if data_band[y][x] == defs.EU_DEM_SEA_LEVEL:
                    tm[y][x].water = True
                else:
                    tm[y][x].elevation = data_band[y][x]
        print("Finished loading Elevation Data")

    # Road Data
    print("Loading Road Data")
    road_data = osmnx.graph_from_bbox(west=Coords.nw_corner[0], north=Coords.nw_corner[1], east=Coords.se_corner[0],
                                      south=Coords.se_corner[1], network_type='drive', retain_all=True,
                                      truncate_by_edge=True)
    transformer = Transformer.from_crs(crs_from=Coords.crs, crs_to=crs, always_xy=True)

    print("Filling TerrainMap with Road Data")
    for road in road_data.edges(data=True):
        if "geometry" in road[2]:
            geo_points = road[2]["geometry"]
            for map_point in get_map_points(geo_points.coords, transformer, transform):
                x = map_point[0]
                y = map_point[1]
                try:
                    tm[y][x].road = True
                except IndexError:  # Road geo goes 1 node beyond boundary because of truncate_by_edge
                    pass

    global loaded_terrain_map
    loaded_terrain_map = tm

    print("Finished loading TerrainMap")
    return tm


if __name__ == "__main__":
    load(elevation_data=defs.FINAL_ELEVATION_DATA)
    print("TerrainMap successfully loaded")
