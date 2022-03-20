from __future__ import annotations  # Required for MapPoint.distance_to(other) type hint

from dataclasses import dataclass
from typing import List, Tuple

from affine import Affine
from osmnx.distance import great_circle_vec
from pyproj import Transformer
from pyproj.enums import TransformDirection


@dataclass
class MapPoint:
    """Represents a 25m × 25m square on the map."""

    water: bool = False
    road: bool = False
    elevation: float = 0


@dataclass
class TerrainMap:
    """Represents a 2D map of MapPoints
       Mapped as y-x, NOT x-y, because rasterio and PIL use y-x order"""

    points: List[List[MapPoint]]
    transformer: Transformer
    affine_transform: Affine

    def __getitem__(self, y: int) -> List[MapPoint]:
        return self.points[y]

    def shape(self) -> Tuple[int, int]:
        if len(self.points) > 0:
            return len(self.points), len(self.points[0])
        else:
            return 0, 0

    def coords_to_map_yx(self, coords: Tuple[float, float]) -> tuple[int, int]:
        assert -180 <= coords[0] <= 180 and -90 <= coords[1] <= 90
        raw_map_point = ~self.affine_transform * self.transformer.transform(coords[0], coords[1])
        return int(raw_map_point[0]), int(raw_map_point[1])

    def map_yx_to_coords(self, yx_position: Tuple[int, int]) -> Tuple[float, float]:
        map_shape = self.shape()
        assert all(yx_position) >= 0 and yx_position[0] < map_shape[0] and yx_position[1] < map_shape[1]
        transformed = self.affine_transform * (yx_position[0] + .5, yx_position[1] + .5)  # Get center of the square.
        return self.transformer.transform(xx=transformed[0], yy=transformed[1], direction=TransformDirection.INVERSE)

    def distance(self, map_point1: Tuple[int, int], map_point2: Tuple[int, int]) -> float:
        return coordinates_distance(self.map_yx_to_coords(map_point1), self.map_yx_to_coords(map_point2))


def create_empty_TerrainMap(y_size: int, x_size: int, transformer: Transformer, affine_transform: Affine) -> TerrainMap:
    assert y_size > 0 and x_size > 0
    return TerrainMap([[MapPoint() for y in range(y_size)] for x in range(x_size)], transformer, affine_transform)


def coordinates_distance(coordinates1: Tuple[float, float], coordinates2: Tuple[float, float]) -> float:
    return great_circle_vec(lng1=coordinates1[0], lat1=coordinates1[1],
                            lng2=coordinates2[0], lat2=coordinates2[1])
