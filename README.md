# Coverage Models for Ad-Hoc 5G Drone Networks #

Ad-hoc 5G networks can be used to control drones in mountainous forested regions, which observe the progress of fires to
plan how to deploy firefighting resources. Since mountainous forested regions do not already have 5G coverage, ad-hoc
base station, located on lorries, with their antennas on the end of tethered drones at high altitude can be situated on
a road anywhere there is no coverage. The objective of this project is to calculate the coverage area of a deployed set
of ad-hoc base stations using propagation path loss models and altitude measurement from Copernicus Maps, so that there
is full coverage over the mountainous region to control the fire observation drones.

## Tools/Data allowed ##

- Copernicus Elevation/Terrain and Impervious Built-up Maps
- MATLAB and/or Python

## Tools/Data used so far ##

- [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html)
- [Python 3.10](https://www.python.org/)
- Elevation data from [Copernicus EU-DEM v1.1](https://land.copernicus.eu/imagery-in-situ/eu-dem/eu-dem-v1.1)
- Road data from [OpenStreetMap (OSM)](https://www.openstreetmap.org/)
- Various Python dependencies to read from the aforementioned datasets [(See Conda environment.yml)](environment.yml)
- [itmlogic](https://github.com/edwardoughton/itmlogic) to implement the Longley-Rice / Irregular Terrain Model
  v1.2.2 [(See pathloss.itmlogic package)](https://github.com/lukect/FYP/tree/master/pathloss/itmlogic)

## Requirements to run ##

- Windows or UNIX OS environment
- [Conda 4.10+](https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html)