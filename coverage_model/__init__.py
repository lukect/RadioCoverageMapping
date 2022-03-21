from typing import Tuple

from PIL import Image
from tqdm import tqdm

import defintions as defs
import terrain_map.load_map
import terrain_map.render_map
from pathloss.itm import itm
from terrain_map.load_map import range_inclusive

coverage_search_range: int = 200

"""
transmitter signal - attenuation = received signal
minimum received signal = noise floor + minimum signal-to-noise

therefore:
transmitter signal - attenuation > noise floor + minimum signal-to-noise
therefore:
- attenuation > noise floor + minimum signal-to-noise - transmitter signal
therefore:
attenuation < transmitter signal - noise floor - minimum signal-to-noise
"""

transmitter_power_dBm: float = 24

minimum_signal_to_noise_dBm: float = 10
noise_floor_dBm: float = -96

max_att_dB: float = transmitter_power_dBm - noise_floor_dBm - minimum_signal_to_noise_dBm


def run(freq_MHz: float, transmitter_coords: Tuple[float, float], transmitter_height: float,
        receiver_height: float):
    if terrain_map.load_map.loaded_terrain_map is None:
        tm = terrain_map.load_map.generate()
    else:
        tm = terrain_map.load_map.loaded_terrain_map
    render = terrain_map.render_map.render(tm, draw_roads=True)

    print('Calculating coverage')
    print('Maximum allowed attenuation = ' + str(max_att_dB) + 'dB')
    transmitter_yx = tm.coords_to_map_yx(transmitter_coords)

    half_range = int(coverage_search_range / 2)

    one_third = 1 / 3

    with tqdm(total=(coverage_search_range + 1) ** 2, smoothing=.025) as progress_bar:
        for y in range_inclusive(transmitter_yx[0] - half_range,
                                 transmitter_yx[0] + half_range):
            for x in range_inclusive(transmitter_yx[1] - half_range,
                                     transmitter_yx[1] + half_range):
                yx = (y, x)
                if tm.exists(yx):
                    attenuation_dB = itm(terrain=tm,
                                         freq_MHz=freq_MHz,
                                         transmitter_coords=transmitter_coords,
                                         receiver_coords=tm.map_yx_to_coords(yx),
                                         transmitter_height=transmitter_height,
                                         receiver_height=receiver_height)
                    if attenuation_dB <= max_att_dB:
                        terrain_map.render_map.draw_red(render, y, x, one_third)
                progress_bar.update(1)
    print('Finished calculating coverage')

    return render


file_path = defs.OUTPUT_DIRECTORY / 'coverage.png'

if __name__ == '__main__':
    transmitter = -5.544048, 56.391095
    img = run(freq_MHz=800, transmitter_coords=transmitter, transmitter_height=10, receiver_height=10)
    image = Image.fromarray(img, mode="RGB")
    image.save(fp=file_path, format="PNG", optimize=True)
