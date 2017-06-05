# coding: utf-8
#
import colander
# from mongoengine import *
# import pymongo
import datetime
import config.cableVariables as cableVar
from unicodedata import numeric, digit

# <------- PREPARER FUNCTIONS

"""Functions to allow the preparing of deserialised data. To be called by the various nodes."""


def preparerconverttozero(value):
    """
    Colander preparer function. Convert zero (0) substitutions to zero (0).
    :param value:
    :return: 0
    """

    zeros = ['-', 'NIL']
    try:
        value.upper()
    except Exception as e:
        return value

    # if value.upper() in zeros:
    #     return 0
    # else:
    #     return value
    return 0

def preparerupper(value):
    """
    Return value.upper()
    :param value:
    :return:
    """
    if not value:
        return 'NIL'
    return value.upper()


def preparerfalse2nil(value):
    """
    Convert FALSE to NIL
    :param value:
    :return:
    """
    if value.upper() is 'FALSE':
        return 'NIL'

    return value


# <----- IMPORT FUNCTION MONGO ENGINE DETAILS


# class CoreDetailsSize(colander.SchemaNode):
#     """
#     Colander core size class. This class allows the specific checking and validation of core size regardless of the cable type.
#     """
#     schema_type = colander.Float()
#     default = cableVar.default_minCableSize
#     title = 'Core Detail Size'
#     missing = 0
#
#     def validator(self, node, cstruct):
#         if cstruct not in cableVar.list_conductorSize:
#             raise colander.Invalid(node, 'Must be in value in list_conductorSize')
#
#     # if details["earthCores.size"] is '-':
#         #     coresize = 0
#         # else:
#         #     coresize = details["earthCores.size"]
#         # if details["earthCores.number"] is '-':
#         #     corenumber = 0
#         # else:
#         #     corenumber = details["earthCores.number"]
#
#         # schema_type=colander.Int
#         # default = 10
#         # title = 'Ranged Int'
#         #
#         # def validator(self, node, cstruct):
#         #     if not 0 < cstruct < 10:
#         #         raise colander.Invalid(node, 'Must be between 0 and 10')


class CoreDetails(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of a cable core.
    It relies on cable variables configuration file being present to check the preferred details.

    :param size: cross sectional area
    :param sizeUnit: cross sectional area unit of measure
    :param number: number of cores
    """

    size = colander.SchemaNode(
        colander.Float(),
        # preparer=test,
        preparer=preparerconverttozero,
        validator=colander.OneOf(cableVar.list_conductorSize),
        default=0,
        missing=colander.required
    )
    sizeUnit = colander.SchemaNode(
        colander.String(),
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_sizeUnit),
        # default=cableVar.default_SizeUnit,
        missing=cableVar.default_SizeUnit
    )
    number = colander.SchemaNode(
        colander.Int(),
        missing=0
    )


class CableInstallDetails(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of the cable installation details.
    It relies on cable variables configuration file being present to check the preferred details.

    :param current: current carrying capacity of the cable. Validator ensures that a negative current cannot be entered.
    :param installTemp: the ambient temperature that the current is based on.
    :param cableArrangement: single core cable arrangements.
    """
    current = colander.SchemaNode(
        colander.Int(),
        validator=colander.Range(min=0)
    )

    installTemp = colander.SchemaNode(
        colander.Int(),
        missing=colander.drop
        # missing=colander.required
    )

    cableArrangement = colander.SchemaNode(
        colander.String(),
        missing=colander.drop,
        # missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_cableArrangement),
        default=cableVar.default_cableArrangement
    )


class CableInsulationDetails(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the cable insulation details.
    It relies on cable variables configuration file being present to check the preferred details.
    :param name:
    :param conductorTemperature:
    :param maxTemperature: # maximum conductor temperature. Assumes degrees C
    """
    name = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_insulationType)
    )

    conductorTemperature = colander.SchemaNode(
        colander.Int(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.Range(min=0)
    )

    maxTemperature = colander.SchemaNode(
        colander.Int(),
        missing=colander.required,
        validator=colander.Range(min=0)
    )

    code = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_insulationCode),
        default=cableVar.default_insulationCode
    )


class CableScreen(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of a cable screen.
    It relies on cable variables configuration file being present to check the preferred details.

    :param name: type of screen
    :param faultWithstand: maximum fault current withstand capability of the screen
    """
    name = colander.SchemaNode(
        colander.String(),
        preparer=[preparerupper, preparerfalse2nil],
        validator=colander.OneOf(cableVar.list_cableScreen),
        # default=cableVar.default_cableScreen
    )

    faultWithstand = colander.SchemaNode(
        colander.Int()
    )


class CoreScreen(colander.MappingSchema):
    """
    Colander Engine data checking class.
    This class defines and checks the details of a core screen.
    It relies on cable variables configuration file being present to check the preferred details.
    :param type: type of screen
    """
    type = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=[preparerupper, preparerfalse2nil],
        validator=colander.OneOf(cableVar.list_coreScreen)
        # default=cableVar.default_coreScreen
    )


class CableImpedance(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of a cable impedance details.
    It relies on cable variables configuration file being present to check the preferred details.

    :param MVAM: Milli-volts per amp-metre
    :param rOhmsPerKM: resistance (ohms/km)
    :param xOhmsPerKM: reactance (ohms/km)
    :param zOhmsPerKM: impedance (ohms/km)
    """
    MVAM = colander.SchemaNode(
        colander.Float(),
        validator=colander.Range(min=0)
    )

    rOhmsPerKM = colander.SchemaNode(
        colander.Float(),
        validator=colander.Range(min=0)
    )

    xOhmsPerKM = colander.SchemaNode(
        colander.Float(),
        validator=colander.Range(min=0)
    )

    zOhmsPerKM = colander.SchemaNode(
        colander.Float(),
        validator=colander.Range(min=0)
    )


class ManufacturerDetails(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of the manufacturer details.
    It relies on cable variables configuration file being present to check the preferred details.

    :param name: Manufacturer's name
    :param partNumber: Manufacturer's part number
    """
    name = colander.SchemaNode(
        colander.String()
    )

    partNumber = colander.SchemaNode(
        colander.String()
    )


class I2T(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of a cable I2T details (i.e. associated with fault current withstand capabilities).
    This class doesn't have much in the way of use at the moment and will require additional work.

    :param kFactor: this will probably have to calculated from a look up table and will be unique to each run
    :param time: this will be a list of time values ranging from 0.0001 to 5 secs. It can zipped with I2T.current shown below.
    :param current: this will be a list of current values that be zipped with I2T.time shown above.
    """
    kFactor = colander.SchemaNode(
        colander.Int(),
        missing=colander.required
    )

    time = colander.SchemaNode(
        colander.List(),
        validator=colander.Range(min=0.0001,
                                 max=5)
    )

    current = colander.SchemaNode(
        colander.List(),
        validator=colander.Range(min=0)
    )


class RevisionDetail(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of a cable's revision details, i.e. when the cable details were updated.
    It relies on cable variables configuration file being present to check the preferred details.

    :param number: Revision number
    :param date: date of the most recent change
    """
    number = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
    )
        # required=True

    date = colander.SchemaNode(
        colander.DateTime(),
        missing=colander.required,
        default=datetime.datetime.now()
    )


class CircuitDetail(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of circuits that the cable is associated with.
    It relies on cable variables configuration file being present to check the preferred details.

    :param circuitVoltage: The voltage of the circuit.
    :param phases: Number of phases the circuit has.
    :param circuitCurrent: Is the circuit ac or dc
    :param deratingFactor: DERATING FACTOR FOR THE CABLE RUN
    """
    circuitVoltage = colander.SchemaNode(
        colander.Int(),
        validator=colander.OneOf(cableVar.list_circuitVoltage)
    )

    phases = colander.SchemaNode(
        colander.Int(),
        missing=colander.required,
        default=3
    )

    circuitCurrent = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_circuitCurrent)
    )

    deratingFactor = colander.SchemaNode(
        colander.Float(),
        missing=colander.required,
        validator=colander.Range(min=0, max=1),
        default=1
    )


class CableDetails(colander.MappingSchema):
    """
    Colander data checking class.
    This class defines and checks the details of a cable.
    It relies on cable variables configuration file being present to check the preferred details.

    :param description: e.g. 3C+E 35mm2 Cu PVC/SWA/PVC 0.6/1kV
    :param cableType: Describes the type of cable e.g. ACTIVE, EARTH, COMMS etc.
    :param circuitType: Describes the type of circuit the cable is used for "SINGLE", "MULTI", "CONTROL", "INSTRUMENT" etc.
    :param conductorMaterial: The material the conductor is made from.
    :param coreArrangement:
    :param activeCores: Embedded document.
    :param neutralCores: Embedded document.
    :param earthCores: Embedded document.
    :param controlCores: Embedded document.
    :param instPairs: Embedded document.
    :param unenclosed_spaced: Embedded document.
    :param unenclosed_surface: Embedded document.
    :param unenclosed_touching: Embedded document.
    :param enclosed_conduit: Embedded document.
    :param enclosed_partial: Embedded document.
    :param enclosed_complete: Embedded document.
    :param buried_direct: Embedded document.
    :param ducts_single: Embedded document.
    :param ducts_per_cable: Embedded document.
    :param insulation: Embedded document.
    :param sheath: Details of the cable sheath
    :param CableScreen: Details of the cable's screen (if any)
    :param CoreScreen: Details of the cable core's screen (if any)
    :param voltRating: Maximum voltage rating fo the cable.
    :param isFlex: Details of how flexiable the cable is.
    :param armoured: Details of the cable's armouring.
    :param impedance: Embedded document.
    :param manufacturer: Details specific to the manufacture of the cable.
    """
    # meta = {'collection': 'Cable'}
    description = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper
        # validator=colander.(  # e.g. 3C+E 35mm2 Cu PVC/SWA/PVC 0.6/1kV
        # required=True
    )

    cableType = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=[preparerupper, preparerfalse2nil],
        validator=colander.OneOf(cableVar.list_cableType),
        default=cableVar.default_cableType
    )

    circuitType = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_circuitType)
    )

    cableShape = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_cableShape),
        default=cableVar.default_cableShape
    )

    conductorMaterial = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_conductorMaterial),
        default=cableVar.default_conductorMaterial
    )

    cableCoreArrangement = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=[preparerupper, preparerfalse2nil],
        validator=colander.OneOf(cableVar.list_coreArrangements),
        default=cableVar.default_cableArrangement
    )
    sheath = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_sheathType)
        # default=cableVar.default_sheathType
    )

    voltRating = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_voltRating)
        # default=cableVar.default_voltRating
    )

    isFlex = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_flexCable)
        # default=cableVar.default_flexCable
    )

    armoured = colander.SchemaNode(
        colander.String(),
        missing=colander.required,
        preparer=preparerupper,
        validator=colander.OneOf(cableVar.list_cableArmour)
        # default=cableVar.default_cableArmour
    )

    impedance = CableImpedance()
    manufacturer = ManufacturerDetails()
    rev = RevisionDetail()
    activeCores = CoreDetails()
    neutralCores = CoreDetails()
    earthCores = CoreDetails()
    controlCores = CoreDetails()
    instPairs = CoreDetails()
    unenclosed_spaced = CableInstallDetails()
    unenclosed_surface = CableInstallDetails()
    unenclosed_touching = CableInstallDetails()
    enclosed_conduit = CableInstallDetails()
    enclosed_partial = CableInstallDetails()
    enclosed_complete = CableInstallDetails()
    unenclosed_partial = CableInstallDetails()
    unenclosed_complete = CableInstallDetails()
    buried_direct = CableInstallDetails()
    underground_ducts = CableInstallDetails()
    ducts_single = CableInstallDetails()
    ducts_per_cable = CableInstallDetails()
    insulation = CableInsulationDetails()
    cableScreen = CableScreen()
    coreScreen = CoreScreen()


# class CableRun(Document):
#     """
#     :param tag: TAGS COULD BE A LIST OF TAGS THAT EQUAL IN NUMBER TO THE NUMBER OF CABLES THAT FORM PART OF THE RUN. THIS WOULD ALLEVIATE THE NEED TO SPECIFY EACH CABLES TAG AND ITS ASSOCIATED CABLE TYPE.
#     :param cable: THE SPECIFIC CABLES THAT MAKE UP THE RUN ARE REFERENCED WITHIN THE LIST. THE LIST WILL NEED TO ALLOW FOR MORE THAN ONE OF A PARTICULAR cable_id TO BE CONTAINED WITHIN IT. THIS WILL ASSIST WITH THE CONSTRUCTION OF MTOS
#     :param cableType:
#     :param circuitType:
#     :param circuitLength:
#     :param numberCables: Number of cables that make up the run. THIS SHOULD BE LINKED TO cables AS DEFINED ABOVE.
#     :param CircuitDetail:
#     :param currentCapacity: THIS IS THE CABLE RUNS CABLE CARRYING CAPACITY BASED ON THE INSTALLATION METHOD, NUMBER OF PARALLEL CABLES AND THE DERATING FACTOR
#     :param installMethod: THIS IS USED TO DETERMINE THE CCC OF THE CABLES IN THE CABLE RUN
#     :param loadedTemp: temperature OF THE CABLE RUN BASED ON ACTUAL LOAD AND CABLE SIZE
#     :param supply: _id of supplying equipment
#     :param load: _id of load equipment
#     """
#     meta = {'collection': 'CableRun'}
#     tag = ListField(required=True)
#     cables = ListField(ReferenceField(Cable))
#                        # required=True)
#     cableType = StringField(required=True,
#                             choices=cableVar.list_cableType)
#     circuitType = StringField(choices=cableVar.list_circuitType)
#     circuitLength = IntField(required=True,
#                              default=0)
#     numberCables = IntField(required=True)
#     CircuitDetail = colander.MappingSchemaField(CircuitDetail)
#     currentCapacity = IntField(required=True)
#     installMethod = StringField(required=True,
#                                 choices=cableVar.list_installMethod)
#     loadedTemp = IntField()
#     supply = StringField(required=True)  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
#     load = StringField(required=True)  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
#     supplyContract = StringField()  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
#     installContract = StringField()  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
#     connectContract = StringField()  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
#     area = StringField()  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
#     MVAM = DecimalField(precision=4)
#     R = DecimalField(precision=4)  # resistance (ohms)
#     X = DecimalField(precision=4)  # reactance (ohms)
#     Z = DecimalField(precision=4)  # impedance (ohms
#     I2T = colander.MappingSchemaField(I2T)
#     revision = colander.MappingSchemaField(RevisionDetail)


# <------- IMPORT FUNCTIONS

# def import_cable_data(db, filepath):
def importCableData(generator):
    """
    Import cable data and add to the database.
    """
    import importCSVData as importCSV
    # import mongoengine as me

    # me.connect(db)
    # generator = importCSV.import_data_generator(filepath)
    try:
        for each in generator:
            if isinstance(each, dict):
                add_cable_dict(each)

            else:
                print("NOT A DICT!!")

    except Exception as e:
        print(e)
    finally:
        generator.close()


def import_cable_run_data():
    """
    """
    pass


def add_cable_dict(importdict):
    """
    This function is designed for the importation of cables importdict from a CSV file. The function will split the dict
    imported from the CSV file into a version that can be serialised as JSON.

    # The function will do some error checking before the MongoEngine's checks. These checks are simple and are
    intended to be basic data entry formating type checks.

    :param importdict: cables importdict contained within a dict.
    """

    """
    Split the imported dictionary into the appropriate sections to allow serialisation if required.
    """
    cable = {}
    cable['description'] = importdict['description'].upper()
    cable['conductorMaterial'] = importdict["conductorMaterial"]
    cable['coreArrangement'] = importdict["coreArrangement"].upper()
    cable['cableType'] = importdict["cableType"].upper()
    if 'cableShape' in cable:
        cable['cableShape'] = importdict["cableShape"].upper()
    cable['circuitType'] = importdict["circuitType"].upper()
    cable['voltRating'] = importdict["voltRating"].upper()
    cable['isFlex'] = importdict["isFlex"].upper()
    cable['sheath'] = importdict["sheath"].upper()
    cable['armoured'] = importdict["armoured"]
    cable['uneclosed_spaced'] = map_dictionary('unenclosed_spaced', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['unenclosed_surface'] = map_dictionary('unenclosed_surface', importdict, 'current', 'installTemp', 'cableArrangement', separator='.' )
    cable['unenclosed_touching'] = map_dictionary('unenclosed_touching', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['enclosed_conduit'] = map_dictionary('enclosed_conduit', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['enclosed_partial'] = map_dictionary('enclosed_partial', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['enclosed_complete'] = map_dictionary('enclosed_complete', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['unenclosed_partial'] = map_dictionary('unenclosed_partial', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['unenclosed_complete'] = map_dictionary('unenclosed_complete', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['buried_direct'] = map_dictionary('buried_direct', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['underground_ducts'] = map_dictionary('underground_ducts', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['ducts_single'] = map_dictionary('ducts_single', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['ducts_per_cable'] = map_dictionary('ducts_per_cable', importdict, 'current', 'installTemp', 'cableArrangement', separator='.')
    cable['activeCores'] = map_dictionary('activeCores', importdict, 'size', 'number', 'sizeUnit', separator='.')
    cable['neutralCores'] = map_dictionary('neutralCores', importdict, 'size', 'number', 'sizeUnit', separator='.')
    cable['earthCores'] = map_dictionary('earthCores', importdict, 'size', 'number', 'sizeUnit', separator='.')
    cable['controlCores'] = map_dictionary('controlCores', importdict, 'size', 'number', 'sizeUnit', separator='.')
    cable['instPairs'] = map_dictionary('instPairs', importdict, 'size', 'number', 'sizeUnit', separator='.')
    cable['insulation'] = map_dictionary('insulation', importdict, 'name', 'code', 'conductorTemperature', 'maxTemperature', separator=',')
    cable['CableScreen'] = map_dictionary('CableScreen', importdict, 'name', 'faultWithstand', separator='.')
    cable['CoreScreen'] = map_dictionary('CoreScreen', importdict, 'type',  separator='.')
    cable['impedance'] = map_dictionary('impedance', importdict, 'MVAM', 'rOhmsPerKM', 'xOhmsPerKM', 'zOhmsPerKM', separator='.')
    cable['manufacturer'] = map_dictionary('manufacturer', importdict, 'name', 'partNumber', separator='.')
    cable['rev'] = map_dictionary('rev', importdict, 'number', 'date', separator='.')
    #     date=datetime.datetime.now()
    # cable.save()

    cstruct = cable
    schema = CableDetails()
    schema.deserialize(cstruct)


def map_dictionary(descrip, supplydict, *args, separator='.'):
    """
    Map the contents of the flat dictionary 'supplydict' with the prefix 'descrip' to the keys contained with '*args'.
    This assumes that keys in '*args' are in 'supplydict'. 'separator' is the separator used to separate the
    description from the keys.
    :param descrip: the prefix contained within 'supplydict' that will be stripped from the
    :param supplydict: the dictionary being passed to the function that contains the values to be mapped to the new
    dictionary.
    :param separator: the separator used to separate the description
    :param args:
    :return:
    """
    x = {}
    for each in args:
        if descrip + separator + each in supplydict:
            x[each] = supplydict[descrip + separator + each]
    return x


def findcable(cabletype, minCCC, circuittype, installmethod, conductormaterial, insulation, sheath, corearrangement=None, voltrating=None, armour=None):
    """
    DB query to find a cable based on the parameters.
    :param cabletype: define the cable type as per list_cableType.
    :param minCCC: the minimum current carrying capacity of the cable.
    :param circuittype: circuit type as per list_circuitType.
    :param installmethod: cable installation method as per the
    :param conductormaterial: material the conductor is manufactured from.
    :param insulation: Cable insulation
    :param sheath: material the cable sheath is made from.
    :param corearrangement: single core cable arrangement.
    :param voltrating: cable insulation voltage capacity
    :param armour: is the cable armoured
    :return:
    """
    if corearrangement == None:
        corearrangement

    voltrating
    armour