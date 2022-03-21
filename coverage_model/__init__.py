from typing import Tuple

from PIL import Image

import defintions as defs
import terrain_map.load_map
import terrain_map.render_map
from pathloss.itm import itm
from terrain_map.load_map import range_inclusive


def run(freq_MHz: float, transmitter_coords: Tuple[float, float], transmitter_height: float, receiver_height: float):
    if terrain_map.load_map.loaded_terrain_map is None:
        tm = terrain_map.load_map.generate()
    else:
        tm = terrain_map.load_map.loaded_terrain_map
    render = terrain_map.render_map.render(tm, draw_roads=True)
    transmitter_yx = tm.coords_to_map_yx(transmitter_coords)
    for y in range_inclusive(transmitter_yx[0] - 50, transmitter_yx[0] + 50):
        for x in range_inclusive(transmitter_yx[1] - 50, transmitter_yx[1] + 50):
            yx = (y, x)
            if tm.exists(yx):
                attenuation_dB = itm(terrain=tm,
                                     freq_MHz=freq_MHz,
                                     transmitter_coords=transmitter_coords,
                                     receiver_coords=tm.map_yx_to_coords(yx),
                                     transmitter_height=transmitter_height,
                                     receiver_height=receiver_height)
                print('Pathloss for ' + str(yx) + ' = ' + str(attenuation_dB))
                if attenuation_dB <= 100:
                    terrain_map.render_map.draw_red(render, y, x)
    return render


file_path = defs.OUTPUT_DIRECTORY / 'coverage.png'

if __name__ == '__main__':
    transmitter = -5.4738459331675635, 56.41555123830365
    img = run(freq_MHz=800, transmitter_coords=transmitter, transmitter_height=10, receiver_height=10)
    image = Image.fromarray(img, mode="RGB")
    image.save(fp=file_path, format="PNG", optimize=True)
