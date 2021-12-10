import crop_elevation
import reproject_elevation


def main():
    crop_elevation.run(show_cropped=True)
    reproject_elevation.reproject_elevation(show_reprojection=True)


if __name__ == "__main__":
    main()
