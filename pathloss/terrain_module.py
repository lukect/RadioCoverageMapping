import math
from typing import Tuple, List

import numpy as np

import terrain_map
from terrain_map import TerrainMap


def interdecile_range(x: List[float]) -> int:
    """
    Get range between bottom 10% and top 10% of values.

    Parameters
    ----------
    x : list
        Terrain profile values.

    Returns
    -------
    interdecile_range : int
        The terrain irregularity parameter.

    """
    q90, q10 = np.percentile(x, [90, 10])

    return int(round(q90 - q10, 0))


def all_data(x):
    """
    Get all data points within mask, with values greater than zero.

    """
    data = x.compressed()
    return data[data > 0]


def determine_num_samples(distance_m: float, max_samples: int = 600) -> int:
    """
    Guarantee a number of samples between 2 and 600.

    Longley-Rice Irregular Terrain Model is limited to only 600
    surface points, so this function ensures this number is not
    passed.

    Parameters
    ----------
    distance_m : float
        Distance between transmitter and receiver in meters.
    max_samples : int
        Less than 2 and above 600 will be ignored

    Returns
    -------
    num_samples : int
        Number of samples between 2 and 600.

    """

    return max(2, min(max_samples, 600, int(math.ceil(distance_m / 25))))


def terrain_p2p(max_samples: int,
                tmap: TerrainMap,
                transmitter_coordinates: Tuple[float, float],
                receiver_coordinates: Tuple[float, float]) \
        -> Tuple[List[float], float]:
    """
    This module takes a set of point coordinates and returns
    the surface profile.

    Parameters
    ----------
    max_samples : int
        Less than 2 and above 600 will be ignored
    tmap : TerrainMap
        Contains elevation data
    transmitter_coordinates : Tuple[float, float]
        Transmitter coordinates
    receiver_coordinates : Tuple[float, float]
        Receiver coordinates

    Returns
    -------
    surface_profile : List
        Contains the surface profile measurements in meters.
    distance_km : float
        Distance in kilometers between the antenna and receiver.

    """

    # Geographic distance
    distance_m = terrain_map.coordinates_distance(transmitter_coordinates, receiver_coordinates)
    distance_km = distance_m / 1e3

    # Interpolate along line to get sampling points
    num_samples = determine_num_samples(distance_m, max_samples)

    transmitter = tmap.coords_to_map_yx(transmitter_coordinates)
    receiver = tmap.coords_to_map_yx(receiver_coordinates)

    diff_y = transmitter[0] - receiver[0]
    diff_x = transmitter[1] - receiver[1]

    surface_profile: List[float] = []
    for n in range(0, num_samples):
        y = int(receiver[0] + ((diff_y / num_samples) * n))
        x = int(receiver[1] + ((diff_x / num_samples) * n))
        surface_profile.append(tmap[y][x].elevation)

    return surface_profile, distance_km
