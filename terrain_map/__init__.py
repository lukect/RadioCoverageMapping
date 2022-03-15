from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class MapPoint:
    """Represents a 25m × 25m square on the map."""

    water: bool = False
    road: bool = False
    elevation: float = 0
    long_lat_coords: Tuple[float, float] = 0, 0


@dataclass
class TerrainMap:
    """Represents a 2D map of MapPoints
       Mapped as y-x, NOT x-y, because rasterio and PIL use y-x order"""

    points: List[List[MapPoint]]

    def __getitem__(self, y: int) -> List[MapPoint]:
        return self.points[y]

    def shape(self) -> Tuple[int, int]:
        if len(self.points) > 0:
            return len(self.points), len(self.points[0])
        else:
            return 0, 0


def create_empty_TerrainMap(y_size: int, x_size: int) -> TerrainMap:
    assert y_size > 0 and x_size > 0
    return TerrainMap([[MapPoint() for y in range(y_size)] for x in range(x_size)])
