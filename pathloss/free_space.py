from math import *

from scipy import constants


def free_space_power_received(distances_meters: float, frequency_hertz: float, power_transmitted_W: float) -> float:
    return power_transmitted_W * ((constants.c / frequency_hertz) ** 2) / ((4 * constants.pi * distances_meters) ** 2)


def free_space_dBm(distances_meters: float, frequency_hertz: float, power_transmitted_W: float) -> float:
    return 10 * log10(free_space_power_received(distances_meters, frequency_hertz, power_transmitted_W) / 0.001)


def free_space_dB(distances_meters: float, frequency_hertz: float) -> float:
    return (20 * log10(distances_meters)) \
           + (20 * log10(frequency_hertz)) \
           + (20 * log10((4 * constants.pi) / constants.c))
