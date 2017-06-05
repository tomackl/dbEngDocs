#
# Coding: UTF-8

# This package allows the conversion of cable data to JSON objects.


def map_dictionary(descrip, supplydict, separator='.', *args):
    """
    Map the contents of the flat dictionary 'supplydict' with the prefix 'descrip' to the keys contained with '*args'.
    This assumes that keys in '*args' are in 'supplydict'. 'separator' is the separator used to separate the description from the keys.
    :param descrip: the prefix contained within 'supplydict' that will be stripped from the
    :param supplydict: the dictionary being passed to the function that contains the values to be mapped to the new dictionary.
    :param separator: the separator used to separate the description
    :param args:
    :return:
    """
    x = {}
    for each in args:
        if descrip + separator + each in supplydict:
            x[each] = supplydict[descrip + separator + each]

    return x


def core_details_dict(descrip, supplydict, *args):
    """
    Provide the core details as a dict and return the dict equivalent that can be passed to MongoDB directly.

    sizeUnit
    number
    :param descrip: Instance of the CoreDetails class being converted.
    :param supplydict: The dictionary being provided to all the
    :return: dict of the core_details that strips out import arrangement.
    """
    x = {}
    if descrip + '.size' in supplydict:
        x['size'] = supplydict[descrip + '.size']
    if descrip + '.sizeUnit' in supplydict:
        x['sizeUnit'] = supplydict[descrip + '.sizeUnit']
    if descrip + '.number' in supplydict:
        x['number'] = supplydict[descrip + '.number']

    return x


def cable_install_details_dict(value):
    """
    Provide the cable installation details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    current
    installTemp
    cableArrangement
    :param value:
    :return: dict
    """


def cable_insulation_details_dict(value):
    """
    Provide the cable insulation details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    name
    conductorTemperature
    maxTemperature
    code
    :param value:
    :return:
    """
    pass


def cable_screen_dict(value):
    """
    Provide the cable screen details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    name
    faultWithstand
    :param value:
    :return:
    """
    pass


def cable_impedance_dict(value):
    """
    Provide the cable impedance details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    MVAM
    rOhmsPerKM
    xOhmsPerKM
    zOhmsPerKM
    :param value:
    :return:
    """
    pass


def manufacturer_details_dict(value):
    """
    Provide the cable manufacturer details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    name
    partNumber
    :param value:
    :return:
    """
    pass


def i2t_dict(value):
    """
    Provide the cable I2T details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    kFactor
    time
    current
    :param value:
    :return:
    """
    pass


def revision_detail_dict(value):
    """
    Provide the cable revision details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    number
    date
    :param value:
    :return:
    """
    pass

def circuit_detail_dict(value):
    """
    Provide the circuit details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    circuitVoltage: The voltage of the circuit.
    phases
    circuitCurrent
    deratingFactor
    :param value:
    :return:
    """
    pass


def cable_details_dict(value):
    """
    Provide the cable details as a dict and return the dict equivalent that can be passed to MongoDB directly.
    description
    cableType
    circuitType
    conductorMaterial
    coreArrangement
    activeCores: Embedded document.
    neutralCores: Embedded document.
    earthCores: Embedded document.
    controlCores: Embedded document.
    instPairs: Embedded document.
    unenclosed_spaced: Embedded document.
    unenclosed_surface: Embedded document.
    unenclosed_touching: Embedded document.
    enclosed_conduit: Embedded document.
    enclosed_partial: Embedded document.
    enclosed_complete: Embedded document.
    buried_direct: Embedded document.
    ducts_single: Embedded document.
    ducts_per_cable: Embedded document.
    insulation: Embedded document.
    sheath
    CableScreen
    CoreScreen
    voltRating
    isFlex
    armoured
    impedance: Embedded document.
    manufacturer
    :param value:
    :return:
    """
    pass

