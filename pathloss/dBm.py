from math import log10


def watts_to_dBm(watts: float) -> float:
    return 10 * log10(watts * 1000)


def dBm_to_watts(dBm: float) -> float:
    return (10 ** (dBm / 10)) / 1000
