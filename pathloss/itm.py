import math
from typing import Tuple

import numpy as np

import terrain_map.load_map
from pathloss import terrain_module
from pathloss.itmlogic.preparatory_subroutines.qlrpfl import qlrpfl
from terrain_map import TerrainMap


def itm(terrain: TerrainMap,
        freq_MHz: float,
        transmitter_coords: Tuple[float, float], receiver_coords: Tuple[float, float],
        transmitter_height: float, receiver_height: float,
        vertical_polarization: bool = False,
        terrain_relative_permittivity: float = 15,
        terrain_conductivity: float = 0.005,
        climate: int = 6
        ) -> float:
    """
        Run itmlogic in point to point (p2p) prediction mode.

        Parameters
        ----------
        terrain : TerrainMap
            The TerrainMap containing elevation data
        freq_MHz : float
            Radio frequency (in MHz)
        transmitter_coords : Tuple[float, float]
            Longitude,Latitude coordinates for transmitter position
        receiver_coords : Tuple[float, float]
            Longitude,Latitude coordinates for receiver position
        transmitter_height : float
            Transmitter's height above ground level
        receiver_height : float
            Receiver's height above ground level
        vertical_polarization : bool
            Polarization of the EM wave (False = Horizontal, True = Vertical)
        terrain_relative_permittivity : float
            Relative-permittivity of the terrain [eps]
        terrain_conductivity : float
            Conductivity of the terrain in S/m [sgm]
        climate : int
            Climate type: (1=equatorial, 2=continental subtropical, 3=maritime subtropical, 4=desert,
            5=continental temperate, 6=maritime temperate overland, 7=maritime temperate oversea (5 is the default)

        Returns
        -------
        output : float
            Pathloss in dB: This is the median attenuation relative to a free space signal that should be observed
            (includes the free space loss)
        """

    # Define a dict for model parameters
    parameters = {'fmhz': freq_MHz,
                  'hg': [transmitter_height, receiver_height],
                  'eps': terrain_relative_permittivity,
                  'sgm': terrain_conductivity,
                  'klim': climate}

    # Polarization selection (0=horizontal, 1=vertical)
    if vertical_polarization:
        parameters['ipol'] = 1
    else:
        parameters['ipol'] = 0

    # Surface refractivity (N-units): also controls effective Earth radius
    parameters['ens0'] = 314

    measured_terrain_profile, distance_km = terrain_module.terrain_p2p(terrain, transmitter_coords, receiver_coords)

    parameters['d'] = distance_km

    # Number of points describing profile -1
    pfl = [len(measured_terrain_profile) - 1, 0]

    for profile in measured_terrain_profile:
        pfl.append(profile)

    # Refractivity scaling ens=ens0*exp(-zsys/9460.)
    # (Average system elev above sea level)
    zsys = 0

    # Note also defaults to a continental temperate climate

    # Setup some intermediate quantities
    # Initial values for AVAR control parameter: LVAR=0 for quantile change,
    # 1 for dist change, 2 for HE change, 3 for WN change, 4 for MDVAR change,
    # 5 for KLIM change
    parameters['lvar'] = 5

    # Inverse Earth radius
    parameters['gma'] = 157E-9

    # Profile range step, select option here to define range step from profile
    # length and # of points
    xkm = 0

    # If XKM is <=0, define range step by taking the profile length/number
    # of points in profile
    if xkm <= 0:
        xkm = parameters['d'] // pfl[0]

        # Range step in meters stored in PFL(2)
        pfl[1] = parameters['d'] * 1000 / pfl[0]

        # Store profile in prop variable
        parameters['pfl'] = pfl
        # Zero out error flag
        parameters['kwx'] = 0
        # Initialize omega_n quantity
        parameters['wn'] = parameters['fmhz'] / 47.7
        # Initialize refractive index properties
        parameters['ens'] = parameters['ens0']

    # Scale this appropriately if zsys set by user
    if zsys != 0:
        parameters['ens'] = parameters['ens'] * math.exp(-zsys / 9460)

    # Include refraction in the effective Earth curvature parameter
    parameters['gme'] = parameters['gma'] * (1 - 0.04665 * math.exp(parameters['ens'] / 179.3))

    # Set surface impedance Zq parameter
    zq = complex(parameters['eps'], 376.62 * parameters['sgm'] / parameters['wn'])

    # Set Z parameter (h pol)
    parameters['zgnd'] = np.sqrt(zq - 1)

    # Set Z parameter (v pol)
    if parameters['ipol'] != 0:
        parameters['zgnd'] = parameters['zgnd'] / zq

    # Flag to tell qlrpfl to set prop.klim=prop.klimx and set lvar to initialize avar routine
    parameters['klimx'] = 0

    # Flag to tell qlrpfl to use prop.mdvar=prop.mdvarx and set lvar to initialize avar routine
    parameters['mdvarx'] = 11

    # Initialization routine for point-to-point mode that sets additional parameters
    # of prop structure
    parameters = qlrpfl(parameters)
    # Here HE = effective antenna heights, DL = horizon distances,
    # THE = horizon elevation angles
    # MDVAR = mode of variability calculation: 0=single message mode,
    # 1=accidental mode, 2=mobile mode, 3 =broadcast mode, +10 =point-to-point,
    # +20=interference

    # Conversion factor to db
    db = 8.685890

    # Free space loss in db
    fs = db * np.log(2 * parameters['wn'] * parameters['dist'])

    return fs + parameters['aref']


# Example test
if __name__ == '__main__':
    tm = terrain_map.load_map.generate()

    transmitter = -5.397801736743245, 56.36349637599007
    receiver = -5.420221902557823, 56.39051697835335

    output = itm(terrain=tm,
                 freq_MHz=800,
                 transmitter_coords=transmitter,
                 receiver_coords=receiver,
                 transmitter_height=10,
                 receiver_height=10)

    print(output)
