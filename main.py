import crop_elevation
import render_elevation_data


def main():
    # reproject_elevation.reproject_elevation(show_reprojection=True)
    crop_elevation.run(show_cropped=True)
    render_elevation_data.save()


if __name__ == "__main__":
    main()
