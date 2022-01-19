import math

import osmnx
import rasterio
from PIL import Image
from affine import Affine
from pyproj import Transformer

import defintions as defs
import defintions.Coordinates as Coords
import render_elevation_data


def get_transform_crs(elevation_data):
    with rasterio.open(elevation_data) as src:
        return src.transform, src.crs


def get_map_points(coords_array, transformer: Transformer, affine_transform: Affine):
    map_points = []

    for coords in coords_array:
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


def yellow(map_img, x: int, y: int):
    map_img[y, x, 0] = 255
    map_img[y, x, 1] = 255
    map_img[y, x, 2] = 0


def range_inclusive(start: int, end: int):
    return range(start, end + 1)


def draw_point(map_img, x: int, y: int):
    for xx in range_inclusive(x - 1, x + 1):
        for yy in range_inclusive(y - 1, y + 1):
            yellow(map_img, xx, yy)


def render():
    road_data = osmnx.graph_from_bbox(west=Coords.nw_corner[0], north=Coords.nw_corner[1], east=Coords.se_corner[0],
                                      south=Coords.se_corner[1], network_type='drive', retain_all=True,
                                      truncate_by_edge=True)

    map_img = render_elevation_data.render(defs.FINAL_ELEVATION_DATA)

    transform, crs = get_transform_crs(defs.FINAL_ELEVATION_DATA)

    transformer = Transformer.from_crs(crs_from=Coords.crs, crs_to=crs, always_xy=True)

    for road in road_data.edges(data=True):
        if "geometry" in road[2]:
            geo_points = road[2]["geometry"]
            for map_point in get_map_points(geo_points.coords, transformer, transform):
                x = map_point[0]
                y = map_point[1]
                try:
                    draw_point(map_img, x, y)
                except IndexError:
                    pass

    return map_img


def view(rendered_road_map=None):
    if rendered_road_map is None:
        rendered_road_map = render()

    img = Image.fromarray(rendered_road_map, mode="RGB")
    img.show(title="View Road Data")

    return


def save(rendered_road_map=None, file_name="map_with_roads.png"):
    if rendered_road_map is None:
        rendered_road_map = render()

    img = Image.fromarray(rendered_road_map, mode="RGB")
    img.save(fp=defs.OUTPUT_DIRECTORY / file_name, format="PNG", optimize=True)

    return


if __name__ == "__main__":
    render = render()
    save(render)
    view(render)
