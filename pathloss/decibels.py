from math import log10

"""dBm: decibel milliwatts"""


def watts_to_dBm(watts: float) -> float:
    return 10 * log10(watts * 1000)


def dBm_to_watts(dBm: float) -> float:
    return (10 ** (dBm / 10)) / 1000


"""dB: decibels"""


def to_dB(value: float) -> float:
    return 10 * log10(value)


def from_dB(dB: float) -> float:
    return 10 ** (dB / 10)
