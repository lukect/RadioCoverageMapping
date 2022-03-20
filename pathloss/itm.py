import math

import numpy as np

import terrain_map.load_map
from pathloss import terrain_module
from pathloss.itmlogic.misc.qerfi import qerfi
from pathloss.itmlogic.preparatory_subroutines.qlrpfl import qlrpfl
from pathloss.itmlogic.statistics.avar import avar


def itmlogic_p2p(main_user_defined_parameters, surface_profile_m):
    """
    Run itmlogic in point to point (p2p) prediction mode.

    Parameters
    ----------
    main_user_defined_parameters : dict
        User defined parameters.
    surface_profile_m : list
        Contains surface profile measurements in meters.

    Returns
    -------
    output : list of dicts
        Contains model output results.

    """
    prop = main_user_defined_parameters

    # DEFINE ENVIRONMENTAL PARAMETERS
    # Terrain relative permittivity
    prop['eps'] = 15

    # Terrain conductivity (S/m)
    prop['sgm'] = 0.005

    # Climate selection (1=equatorial,
    # 2=continental subtropical, 3=maritime subtropical,
    # 4=desert, 5=continental temperate,
    # 6=maritime temperate overland,
    # 7=maritime temperate, oversea (5 is the default)
    prop['klim'] = 6

    # Surface refractivity (N-units): also controls effective Earth radius
    prop['ens0'] = 314

    # DEFINE STATISTICAL PARAMETERS
    # Confidence  levels for predictions
    qc = [50, 90, 10]

    # Reliability levels for predictions
    qr = [1, 10, 50, 90, 99]

    # Number of points describing profile -1
    pfl = [len(surface_profile_m) - 1, 0]

    for profile in surface_profile_m:
        pfl.append(profile)

    # Refractivity scaling ens=ens0*exp(-zsys/9460.)
    # (Average system elev above sea level)
    zsys = 0

    # Note also defaults to a continental temperate climate

    # Setup some intermediate quantities
    # Initial values for AVAR control parameter: LVAR=0 for quantile change,
    # 1 for dist change, 2 for HE change, 3 for WN change, 4 for MDVAR change,
    # 5 for KLIM change
    prop['lvar'] = 5

    # Inverse Earth radius
    prop['gma'] = 157E-9

    # Conversion factor to db
    db = 8.685890

    # Number of confidence intervals requested
    nc = len(qc)

    # Number of reliability intervals requested
    nr = len(qr)

    # Length of profile in km
    dkm = prop['d']

    # Profile range step, select option here to define range step from profile
    # length and # of points
    xkm = 0

    # If DKM set <=0, find DKM by mutiplying the profile step by number of
    # points (not used here)
    if dkm <= 0:
        dkm = xkm * pfl[0]

    # If XKM is <=0, define range step by taking the profile length/number
    # of points in profile
    if xkm <= 0:
        xkm = dkm // pfl[0]

        # Range step in meters stored in PFL(2)
        pfl[1] = dkm * 1000 / pfl[0]

        # Store profile in prop variable
        prop['pfl'] = pfl
        # Zero out error flag
        prop['kwx'] = 0
        # Initialize omega_n quantity
        prop['wn'] = prop['fmhz'] / 47.7
        # Initialize refractive index properties
        prop['ens'] = prop['ens0']

    # Scale this appropriately if zsys set by user
    if zsys != 0:
        prop['ens'] = prop['ens'] * math.exp(-zsys / 9460)

    # Include refraction in the effective Earth curvature parameter
    prop['gme'] = prop['gma'] * (1 - 0.04665 * math.exp(prop['ens'] / 179.3))

    # Set surface impedance Zq parameter
    zq = complex(prop['eps'], 376.62 * prop['sgm'] / prop['wn'])

    # Set Z parameter (h pol)
    prop['zgnd'] = np.sqrt(zq - 1)

    # Set Z parameter (v pol)
    if prop['ipol'] != 0:
        prop['zgnd'] = prop['zgnd'] / zq

    # Flag to tell qlrpfl to set prop.klim=prop.klimx and set lvar to initialize avar routine
    prop['klimx'] = 0

    # Flag to tell qlrpfl to use prop.mdvar=prop.mdvarx and set lvar to initialize avar routine
    prop['mdvarx'] = 11

    # Convert requested reliability levels into arguments of standard normal distribution
    zr = qerfi([x / 100 for x in qr])
    # Convert requested confidence levels into arguments of standard normal distribution
    zc = qerfi([x / 100 for x in qc])

    # Initialization routine for point-to-point mode that sets additional parameters
    # of prop structure
    prop = qlrpfl(prop)

    # Here HE = effective antenna heights, DL = horizon distances,
    # THE = horizon elevation angles
    # MDVAR = mode of variability calculation: 0=single message mode,
    # 1=accidental mode, 2=mobile mode, 3 =broadcast mode, +10 =point-to-point,
    # +20=interference

    # Free space loss in db
    fs = db * np.log(2 * prop['wn'] * prop['dist'])

    # Used to classify path based on comparison of current distance to computed
    # line-of-site distance
    q = prop['dist'] - prop['dlsa']

    # Scaling used for this classification
    q = max(q - 0.5 * pfl[1], 0) - max(-q - 0.5 * pfl[1], 0)

    # Report dominant propagation type predicted by model according to parameters
    # obtained from qlrpfl
    if q < 0:
        print('Line of sight path')
    elif q == 0:
        print('Single-horizon path')
    else:
        print('Double-horizon path')
    if prop['dist'] <= prop['dlsa']:
        print('Diffraction is the dominant mode')
    elif prop['dist'] > prop['dx']:
        print('Tropospheric scatter is the dominant mode')

    print('Estimated quantiles of basic transmission loss (db)')
    print('Free space value {} db'.format(str(fs)))

    print('Confidence levels {}, {}, {}'.format(
        str(qc[0]), str(qc[1]), str(qc[2])))

    # Confidence  levels for predictions
    qc = [50, 90, 10]

    # Reliability levels for predictions
    qr = [1, 10, 50, 90, 99]

    output = []
    for jr in range(0, nr):
        for jc in range(0, nc):
            # Compute corrections to free space loss based on requested confidence
            # and reliability quantities
            avar1, prop = avar(zr[jr], 0, zc[jc], prop)
            output.append({
                'distance_km': prop['d'],
                'reliability_level_%': qr[jr],
                'confidence_level_%': qc[jc],
                'propagation_loss_dB': fs + avar1  # Add free space loss and correction
            })

    return output


if __name__ == '__main__':
    tm = terrain_map.load_map.generate()

    # DEFINE MAIN USER PARAMETERS
    # Define an empty dict for user defined parameters
    main_user_defined_parameters = {}

    # Define radio operating frequency (MHz)
    main_user_defined_parameters['fmhz'] = 800

    # Define antenna heights - Transmitter height (m) # Receiver height (m)
    main_user_defined_parameters['hg'] = [10, 10]

    # Polarization selection (0=horizontal, 1=vertical)
    main_user_defined_parameters['ipol'] = 0

    transmitter = -5.397801736743245, 56.36349637599007
    receiver = -5.420221902557823, 56.39051697835335

    measured_terrain_profile, distance_km = terrain_module.terrain_p2p(tm, transmitter, receiver)

    main_user_defined_parameters['d'] = distance_km
    print('Distance is {}km'.format(distance_km))

    # Check (out of interest) how many measurements are in each profile
    print('len(measured_terrain_profile) {}'.format(len(measured_terrain_profile)))

    # Run model and get output
    output = itmlogic_p2p(main_user_defined_parameters, measured_terrain_profile)

    print(output)
