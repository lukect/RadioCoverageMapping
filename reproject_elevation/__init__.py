import rasterio
from pyproj import CRS
from rasterio.plot import show
from rasterio.warp import calculate_default_transform, reproject, Resampling

import defintions as defs


def match(crs0, crs1):
    crs_a = CRS.from_user_input(crs0)
    crs_b = CRS.from_user_input(crs1)

    if crs_a.equals(crs_b):
        return True

    if crs_a.to_3d() == crs_b.to_3d():
        return True

    if crs_a.to_epsg(min_confidence=50) == crs_b.to_epsg(min_confidence=50):
        return True

    if crs_a.to_proj4() == crs_b.to_proj4():
        return True

    return False


def run(show_reprojection: bool = True):
    with rasterio.open(defs.ORIGINAL_ELEVATION_DATA) as src:
        if not match(src.crs, defs.PROJECT_CRS):
            transform, width, height = calculate_default_transform(
                src.crs, defs.PROJECT_CRS, src.width, src.height, *src.bounds)
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': defs.PROJECT_CRS,
                'transform': transform,
                'width': width,
                'height': height
            })

            with rasterio.open(defs.REPROJECTED_ELEVATION_DATA, 'w', **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rasterio.band(src, i),
                        destination=rasterio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_transform=transform,
                        dst_crs=defs.PROJECT_CRS,
                        resampling=Resampling.nearest)
            if show_reprojection:
                with rasterio.open(defs.REPROJECTED_ELEVATION_DATA) as final:
                    show(final)


if __name__ == '__main__':
    run()
