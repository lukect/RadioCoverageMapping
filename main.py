"""
Coverage Models for Ad-Hoc 5G Drone Networks

Ad-hoc 5G networks can be used to control drones in mountainous forested regions, which observe the progress of
fires to plan how to deploy firefighting resources. Since mountainous forested regions do not already have 5G 
coverage, ad-hoc base station, located on lorries, with their antennas on the end of tethered drones at high altitude 
can be situated on a road anywhere there is no coverage. The objective of this project is to calculate the coverage 
area of a deployed set of ad-hoc base stations using propagation path loss models and altitude measurement from 
Copernicus Maps, so that there is full coverage over the mountainous region to control the fire observation drones.
"""

import crop_elevation
from terrain_map import render_map


def main():
    # reproject_elevation.reproject_elevation(show_reprojection=True)
    crop_elevation.run(show_cropped=True)
    render_map.save()


if __name__ == "__main__":
    main()
