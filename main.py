import crop_elevation
import reproject_elevation


def main():
    reproject_elevation.reproject_elevation(show_reprojection=True)
    crop_elevation.run(show_cropped=True)


if __name__ == "__main__":
    main()
