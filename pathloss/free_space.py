from scipy import constants

from decibels import *


def free_space_power_received(distances_meters: float, frequency_hertz: float, power_transmitted_W: float) -> float:
    return power_transmitted_W * ((constants.c / frequency_hertz) ** 2) / ((4 * constants.pi * distances_meters) ** 2)


def free_space_dBm(distances_meters: float, frequency_hertz: float, power_transmitted_W: float) -> float:
    return watts_to_dBm(free_space_power_received(distances_meters, frequency_hertz, power_transmitted_W))


def free_space_dB(distances_meters: float, frequency_hertz: float) -> float:
    return (2 * to_dB(distances_meters)) \
           + (2 * to_dB(frequency_hertz)) \
           + (2 * to_dB((4 * constants.pi) / constants.c))


def free_space_distance(attenuation_dB: float, frequency_hertz: float) -> float:
    return 10 ** ((attenuation_dB + (2 * to_dB(constants.c / frequency_hertz)) - (2 * to_dB(4 * constants.pi))) / 20)


if __name__ == '__main__':
    print(free_space_distance(109, 800_000_000))
    print(free_space_dB(43, 40000))
    print(free_space_dBm(599, 532_000_000, 1))
