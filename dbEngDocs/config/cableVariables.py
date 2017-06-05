fileDetails = {
    "DB": "dbEngDocs",
    "collection": "Cable",
    "file": ".config"
    }

# TODO: Consider creating a collection that stores these values in it and provides more information about specific variables than currently contained within this file.

"""
CableType allows identification of the primary purpose of the cable. This is not a fixed requirement but is intended to
allow a high level filter of cable types. Single core cables will active and neutral conductors to be differentiated by
 active and neutral conductor CSA.
"""

# TODO: Provide a list of single core cables that have a neutral conductor size.
# TODO: Update AS3008.1.1 cables to have AS3008.1.1 as the manufacturer.

list_cableType = [
    # The general type of cable.
    "ACTIVE", # All power (LV and HV) cables. In the case of single core cables these the active conductors.
    "NEUTRAL", # A single core cable actiing as a neutral conductor of a power circuit.
    "POWER",
    "EARTH",
    "CONTROL",
    "INSTRUMENT",
    "DATA",
    "COMMS",
    "-"
  ]

default_cableType = "POWER"

"""
The default maximum number of parallel cables that can be run in parallel.
"""
default_cablesMaxParallel = 4
default_cableAllowParallelMulti = True

"""
coreType is type of cable core. At this stage deals only with power cable cores. 
"""

list_coreType = [
    'ACTIVE',
    'NEUTRAL',
    'EARTH'
]

default_coreType = [
    'ACTIVE'
]

list_cableShape = [
    "CIRCULAR",
    "FLAT"
]

default_cableShape = "CIRCULAR"

""""
CircuitType defines whether the circuit will be a single or multi-phase lower cable or a data/instrumentation/fibre
  optic cable.
While circuitType is related to voltage, it is not determined by voltage.
"""
# Corresponds to coreArrangement and cable rating.
list_circuitType = [
    "SINGLE",   # Single phase circuits
    "MULTI",    # Multi-phase circuits
    "CONTROL",
    "INSTRUMENT",
    "COMMS",
    "DATA"
]

default_circuitType = 'MULTI'

list_conductorMaterial = [
    "CU",
    "AL"
]

default_conductorMaterial = "CU"

list_installMethod = [
    "UNENCLOSED_SPACED",
    "UNENCLOSED_SURFACE",
    "UNENCLOSED_TOUCHING",
    "ENCLOSED_CONDUIT",
    "ENCLOSED_PARTIAL",
    "ENCLOSED_COMPLETE",
    "UNENCLOSED_PARTIAL",
    "UNENCLOSED_COMPLETE",
    "BURIED_DIRECT",
    "UNDERGROUND_DUCTS",
    "DUCTS_SINGLE",
    "DUCTS_PER_CABLE"
]

default_installMethod = "UNENCLOSED_TOUCHING"


list_cableArrangement = [
    "NIL",
    "FLAT",
    "TREFOIL"
]

default_cableArrangement = "NIL"

list_sheathType = [
    "PVC",
    "HDPE",
    "EPR",
    "UNSHEATHED"
]
default_sheathType = "PVC"

list_insulationType = [
    "XLPE",
    "PVC",
    "PILS",
    "EPR"
]

default_insulationType = "PVC"

# Insulation corresponds to insulationType and conductor temperatures
list_insulationCode = [
    "X-90",
    "V-90",
    "V-90RP",
    "V-75"
]

default_insulationCode = "V-90"

# voltRating correspoonds to circuit voltage
list_voltRating = [
    "300/500V",
    "450/750V",
    "110V",
    "0.6/1KV",
    "6.35/11KV",
    "12.7/22KV"
]

default_voltRating = "0.6/1KV"

list_circuitVoltage = [
    0,
    12,
    24,
    48,
    110,
    230,
    240,
    380,
    400,
    415,
    690,
    1000,
    3300,
    6600,
    11000,
    22000,
    33000
]

list_circuitCurrent = [
      "AC",
      "DC"
]

list_conductorSize = [
    0,
    1,
    1.5,
    2.5,
    4,
    6,
    10,
    16,
    25,
    35,
    50,
    70,
    95,
    120,
    150,
    185,
    240,
    300,
    400,
    500,
    630
]

default_minCableSize = 4

default_minCableSingleCoreSize = 120

list_sizeUnit = [
    "MM2",
    '-'
]

default_sizeUnit = "MM2"

list_coreArrangement = [
    "-",
    "1C",
    "2C",
    "3C",
    "2C+E",
    "3C+E",
    "3C+3E",
    "4C+E",
    "5C+E",
    "10C+E",
    "20C+E",
    "50C+E",
    "1PR",
    "2PR",
    "4PR",
    "5PR",
    "6PR",
    "10PR",
    "12PR",
    "20PR",
    "1TRI",
    "2TRI",
    "4TRI",
    "5TRI",
    "6TRI",
    "10TRI",
    "12TRI",
    "20TRI"
]

default_coreArrangement = '3C+E'




list_coreName = [
    '-',
    'CORE',
    'PAIR', # Instrument pairs
    'TRIPLE' # Instrument triple
]

default_coreName = 'CORE'

list_cableArmour = [
    "NIL",
    "SWA",
    "DWA"
]

default_cableArmour = "NIL"

list_cableScreen = [
    "NIL",
    "DCT",
    "OS"
]

default_cableScreen = "NIL"

list_coreScreen = [
    "NIL",
    "IS"
]

default_coreScreen = "NIL"

list_power = {
    "WATT": 1,
    "WATTS": 1,
    "W": 1,
    "KILO-WATT": 1000,
    "KILO-WATTS": 1000,
    "KW": 1000,
    "MEGA-WATT": 1000000,
    "MEGA-WATTS": 1000000,
    "MW": 1000000,
    "VOLT-AMPS": 1,
    "VOLT-AMP": 1,
    "VA": 1,
    "KILO-VOLT-AMP": 1000,
    "KILO-VOLT-AMPS": 1000,
    "KVA": 1000,
    "MEGA-VOLT-AMP": 1000000,
    "MEGA-VOLT-AMPS": 1000000,
    "MVA": 1000000,

}

list_flexCable = [
    "TRUE",
    "FALSE"
]

default_flexCable = "FALSE"
