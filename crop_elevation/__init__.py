import rasterio
from pyproj import Transformer
from rasterio.plot import show
from rasterio.windows import Window

import defintions as defs
from defintions import Coordinates


def run(show_cropped: bool = True):
    with rasterio.open(defs.REPROJECTED_ELEVATION_DATA) as elevation_data:
        transformer = Transformer.from_crs(crs_from=Coordinates.crs, crs_to=elevation_data.crs, always_xy=True)
        affine_nw = transformer.transform(Coordinates.nw_corner[0], Coordinates.nw_corner[1])
        affine_se = transformer.transform(Coordinates.se_corner[0], Coordinates.se_corner[1])

        min_y, min_x = elevation_data.index(affine_nw[0], affine_nw[1])
        max_y, max_x = elevation_data.index(affine_se[0], affine_se[1])

        diff_x = max_x - min_x
        diff_y = max_y - min_y

        window = Window(col_off=min_x, row_off=min_y, width=diff_x, height=diff_y)
        transform = elevation_data.window_transform(window)

        new_profile = elevation_data.profile
        new_profile.update({
            'width': diff_x,
            'height': diff_y,
            'transform': transform
        })

        with rasterio.open(defs.FINAL_ELEVATION_DATA, 'w', **new_profile) as crop:
            crop.write(elevation_data.read(window=window))
        if show_cropped:
            with rasterio.open(defs.FINAL_ELEVATION_DATA) as cropped:
                show(cropped)


if __name__ == "__main__":
    run()
