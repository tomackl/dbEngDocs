#! /Library/Frameworks/Python.framework/Versions/3.3/bin/python3
# coding: utf-8

kw2hp = 1.34102209
hp2kw = 0.745699872


def kwtohp(kw):
    """
    Convert kw to horse-power.
    """
    return kw * kw2hp


def hptokw(hp):
    """
    Convert horse-power to kW.
    """
    return hp * hp2kw


def mvamvoltagedrop(cablelength, amps, Vc):
    """
    Calculate the voltage drop based on the cable milli-volt per amp-metre
    value.
    :param Vc: The cable's milli-volt per amp-metre value
    :param cablelength: Cable length in metres.
    :param amps: The load current in amps.
    :return Vd: The volt drop across the cable
    """
    return (amps * cablelength * Vc) / 1000.0

def ohmvoltagedrop(cablelength, amps, Zc=0, Rc=0, Xc=0):
    """
    Calculate the voltage drop based on the cable's impedance.
    :param cablelength: Cable length in metres
    :param amps:
    :param Zc: provided in ohms/km
    :param Rc: provided in ohms/km
    :param Xc: provided in ohms/km
    :return Vd: The volt drop across the cable.
    """
    if (Rc != 0) or (Xc != 0):
        zc_m = complex(Rc/1000, Xc/1000)

    elif isinstance(Zc, complex) and (Zc != 0):
        zc_m = Zc/1000

    return abs(cablelength * zc_m * amps)


def mVamMaxCableLength(Vc, maxVd, amps):
    """
    Calculate the maximum cable length (metres) based on it's milli-volt per amp-metre
    value and the load current (amps).
    :param Vc:  The cable's milli-volt per amp-metre value
    :param maxVd: The maximum allowable volt drop along the cable (volts)
    :param amps: The load current in amps
    :return: the maximum cable in metres
    """
    return (maxVd * 1000) / (amps * Vc)

def motorapparantpower(kW, eff, pf):
    """
    Calculate a motor's apparant power S.
    :param kW:
    :param eff:
    :param pf:
    :return:
    """
    return kW / (eff * pf)

def motor_iflc(apparentpower, voltage, phases):
    """
    calculate the motor's full load current.
    :param apparentpower: Apparent power
    :param voltage: phase to phase voltage
    :param phases: number of phases, i.e. 1 or 3
    :return:
    """
    from math import sqrt

    if phases is 1:
        return apparentpower / voltage

    if phases is 3:
        return apparentpower / (3**0.5 * voltage)

def calculateimpedance(r=None, x=None, z=None):
    """
    Using two resistance values calculate the third. The function requires that
    two of the following resistance type be passed, in order to calculate the
    third: R, X nd Z.
    :param r: resistance
    :param x: reactance
    :param z: impedance
    :return: returns a list in the form [r, x, z]
    """
    from cmath import sqrt
    if ((r is not None) or (r != 0.0)) and \
            ((x is not None) or (x != 0.0)) and \
            ((z is None) or (z == 0.0)):
        return [r, x, abs(complex(r, x))]

    elif ((r is not None) or (r != 0.0)) and \
            ((z is not None) or (z != 0.0)) and \
            ((x is None) or (x == 0.0)):
        return [r, abs(sqrt(r**2 - z**2)), z]

    elif ((x is not None) or (x != 0.0)) and \
            ((z is not None) or (z != 0.0)) and \
            ((r is None) or (r == 0.0)):
        return [abs(sqrt(x**2 - z**2)), x, z]

    # GET THE FEELING THAT AN EXCEPTION SHOULD BE RAISED HERE.


def derate(value, deratefactor):
    """
    Calculate the derated value for a value and the derating factor.
    :param value:
    :param deratefactor:
    """
    return value * deratefactor

def calculateparallelohms(ohms):
    """
    Calculate the ohms of a series of parallel resistances. The individual values do not need to be the same as would be
    expected in a cable run. Resistances provided as a per unit length (e.g. ohms/km) do _not_ consider the per unit f
    actor which will need to be addressed separately.
    :param ohms: a list of the resistances.
    :return:
    """
    x = 0
    try:
        x = ohms.pop()
        for each in ohms:
            x = (x * each) / (x + each)
    except Exception as e:
        pass
        # print(e)
    return x
