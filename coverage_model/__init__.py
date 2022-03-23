import math
from typing import Tuple

from PIL import Image
from tqdm import tqdm

import defintions as defs
import terrain_map.load_map
import terrain_map.render_map
from pathloss.free_space import free_space_distance
from pathloss.itm import itm
from terrain_map.load_map import range_inclusive

one_third = 1 / 3

"""
transmitter signal - attenuation = received signal
minimum required signal reception = noise floor + minimum signal-to-noise

therefore:
transmitter signal - attenuation > noise floor + minimum signal-to-noise
therefore:
- attenuation > noise floor + minimum signal-to-noise - transmitter signal
therefore:
attenuation < transmitter signal - noise floor - minimum signal-to-noise
"""

transmitter_power_dBm: float = 23
transmitter_gain_dB: float = 20
receiver_gain_dB: float = 20

minimum_signal_to_noise_dBm: float = 10
noise_floor_dBm: float = -100

max_att_dB: float = transmitter_power_dBm + transmitter_gain_dB + receiver_gain_dB \
                    - noise_floor_dBm - minimum_signal_to_noise_dBm


def run(freq_MHz: float, transmitter_coords: Tuple[float, float],
        transmitter_height: float, receiver_height: float,
        max_surface_terrain_profile_samples: int = 600):
    if terrain_map.load_map.loaded_terrain_map is None:
        tm = terrain_map.load_map.generate()
    else:
        tm = terrain_map.load_map.loaded_terrain_map
    render = terrain_map.render_map.render(tm, draw_roads=True)

    transmitter_yx = tm.coords_to_map_yx(transmitter_coords)
    assert tm.exists(transmitter_yx)

    print('Calculating coverage')
    print('Maximum allowed attenuation = ' + str(max_att_dB) + 'dB')

    shape = tm.shape()

    max_dist = int(round(free_space_distance(max_att_dB, freq_MHz * 1_000_000)))
    steps = round(max_dist / 25)
    _y = range_inclusive(max(transmitter_yx[0] - steps, 0), min(transmitter_yx[0] + steps, shape[0] - 1))
    _x = range_inclusive(max(transmitter_yx[1] - steps, 0), min(transmitter_yx[1] + steps, shape[1] - 1))
    calcs = len(_y) * len(_x)
    print('Calculating up to ' + str(max_dist) + 'm away (' + str(calcs) + ' calculations)')
    with tqdm(total=calcs, smoothing=.025) as progress_bar:
        for y in _y:
            for x in _x:
                dist_from_transmitter = math.sqrt(((transmitter_yx[0] - y) ** 2) + ((transmitter_yx[1] - x) ** 2))
                if 0 < dist_from_transmitter <= 4:
                    terrain_map.render_map.draw_deep_pink(render, y, x)
                elif 4 <= dist_from_transmitter <= steps:  # ITM requires min 100m distance
                    attenuation_dB = itm(terrain=tm,
                                         freq_MHz=freq_MHz,
                                         transmitter_coords=transmitter_coords,
                                         receiver_coords=tm.map_yx_to_coords((y, x)),
                                         transmitter_height=transmitter_height,
                                         receiver_height=receiver_height,
                                         max_samples=max_surface_terrain_profile_samples)
                    if attenuation_dB <= max_att_dB:
                        terrain_map.render_map.draw_red(render, y, x, one_third)
                progress_bar.update(1)
    print('Finished calculating coverage')

    return render


if __name__ == '__main__':
    high = -5.308657, 56.381646
    oban_out = -5.455720, 56.427951
    lismore_lighthouse = -5.586764910128153, 56.46462979716061

    transmitter = lismore_lighthouse
    freq_MHz = 3_800
    transmitter_height = 5
    receiver_height = 300

    img = run(freq_MHz=freq_MHz, transmitter_coords=transmitter,
              transmitter_height=transmitter_height, receiver_height=receiver_height,
              max_surface_terrain_profile_samples=100)
    image = Image.fromarray(img, mode="RGB")
    file = defs.OUTPUT_DIRECTORY / ("coverage_f" + str(freq_MHz)
                                    + "_th" + str(transmitter_height)
                                    + "_rh" + str(receiver_height)
                                    + "_coords" + str(transmitter) + ".png")
    image.save(fp=file, format="PNG", optimize=True)
