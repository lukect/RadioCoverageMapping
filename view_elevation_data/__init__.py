import rasterio

import defintions as defs


def view(data):
    with rasterio.open(data) as src:
        data_band = src.read(1)
        print(data_band.shape)
        for x in data_band:
            for y in x:
                print(y)
                # every x-y is a height. not sure if the x is really the horizontal here.


if __name__ == "__main__":
    view(defs.FINAL_ELEVATION_DATA)
