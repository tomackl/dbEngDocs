# coding: utf-8
#
from mongoengine import *
#import pymongo
import datetime
import config.cableVariables as cableVar


"""
Global variables are intended to be accessed from a module wide context. The following isn't going to work in it's current form and will need to be better considered.
"""


class coreDetails(EmbeddedDocument):
    """
    :param size: cross sectional area
    :param sizeUnit: cross sectional area unit of measure
    :param number: number of cores
    """
    size = DecimalField(precision=1,
                        choices=cableVar.list_conductorSize,
                        default=cableVar.default_minCableSize)
    sizeUnit = StringField(choices=cableVar.list_sizeUnit,
                           default=cableVar.default_SizeUnit)
    number = IntField()


class cableInstallDetails(EmbeddedDocument):
    """
    :param current: current carrying capacity of the cable
    :param installTemp: the ambient temperature that the current is based on.
    :param cableArrangement: single core cable arrangements.
    """
    current = IntField(required=True)
    installTemp = IntField(required=True)
    cableArrangement = StringField(choices=cableVar.list_cableArrangement)


class cableInsulationDetails(EmbeddedDocument):
    """
    :param name:
    :param conductorTemperature:
    :param maxTemperature: # maximum conductor temperature. Assumes degrees C
    """
    name = StringField(required=True,
                       choices=cableVar.list_insulationType)
    conductorTemperature = IntField(required=True)
    maxTemperature = IntField(required=True)
    code = StringField(required=True,
                       choices=cableVar.list_insulationCode,
                       default=cableVar.default_insulationCode)


class cableScreen(EmbeddedDocument):
    """
    :param name: type of screen
    :param faultWithstand: maximum fault current withstand capability of the screen
    """
    name = StringField(choices=cableVar.list_cableScreen,
                       default=cableVar.default_cableScreen)
    faultWithstand = IntField()


class coreScreen(EmbeddedDocument):
    """
    :param type: type of screen
    """
    type = StringField(choices=cableVar.list_coreScreen,
                       default=cableVar.default_coreScreen)


class cableImpedance(EmbeddedDocument):
    """
    :param MVAM: Milli-volts per amp-metre
    :param rOhmsPerKM: resistance (ohms/km)
    :param xOhmsPerKM: reactance (ohms/km)
    :param zOhmsPerKM: impedance (ohms/km)
    """
    MVAM = DecimalField(precision=4)
    rOhmsPerKM = DecimalField(precision=4)
    xOhmsPerKM = DecimalField(precision=4)
    zOhmsPerKM = DecimalField(precision=4)


class manufacturerDetails(EmbeddedDocument):
    """
    :param name: Manufacturer's name
    :param partNumber: Manufacturer's part number
    """
    name = StringField()
    partNumber = StringField()


class i2t(EmbeddedDocument):
    """
    :param kFactor: this will probably have to calculated from a look up table and will be unique to each run
    :param time: this will be a list of time values ranging from 0.0001 to 5 secs. It can zipped with I2T.current shown below.
    :param current: this will be a list of current values that be zipped with I2T.time shown above.
    """
    kFactor = IntField(required=True)
    time = ListField(min_value=0.0001,
                     max_value=5,
                     precision=4)
    current = ListField(min_value=0)


class revisionDetail(EmbeddedDocument):
    """
    :param number: Revision number
    :param date: date of the most recent change
    """
    number = StringField(required=True),
    date = DateTimeField(default=datetime.datetime.now())


class circuitDetail(EmbeddedDocument):
    """
    :param circuitVoltage: The voltage of the circuit.
    :param phases: Number of phases the circuit has.
    :param circuitCurrent: Is the circuit ac or dc
    :param deratingFactor: DERATING FACTOR FOR THE CABLE RUN
    """
    circuitVoltage = IntField(choices=cableVar.list_circuitVoltage)
    phases = IntField(required=True,
                      default=3)
    circuitCurrent = StringField(required=True,
                                 choices=cableVar.list_circuitCurrent)
    deratingFactor = FloatField(default=1)


class cableDetails(Document):
    """
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
    meta = {'collection': 'Cable'}
    description = StringField() # e.g. 3C+E 35mm2 Cu PVC/SWA/PVC 0.6/1kV
    cableType = StringField(required=True,
                            choices=cableVar.list_cableType,
                            default=cableVar.default_cableType)
    circuitType = StringField(choices=cableVar.list_circuitType)
    conductorMaterial = StringField(choices=cableVar.list_conductorMaterial,
                                    default=cableVar.default_conductorMaterial)
    cableCoreArrangement = StringField(choices=cableVar.list_coreArrangements)
    activeCores = EmbeddedDocumentField(coreDetails)
    neutralCores = EmbeddedDocumentField(coreDetails)
    earthCores = EmbeddedDocumentField(coreDetails)
    controlCores = EmbeddedDocumentField(coreDetails)
    instPairs = EmbeddedDocumentField(coreDetails)
    # current = EmbeddedDocumentListField(CableInstallDetails)
    unenclosed_spaced = EmbeddedDocumentField(cableInstallDetails)
    unenclosed_surface = EmbeddedDocumentField(cableInstallDetails)
    unenclosed_touching = EmbeddedDocumentField(cableInstallDetails)
    enclosed_conduit = EmbeddedDocumentField(cableInstallDetails)
    enclosed_partial = EmbeddedDocumentField(cableInstallDetails)
    enclosed_complete = EmbeddedDocumentField(cableInstallDetails)
    buried_direct = EmbeddedDocumentField(cableInstallDetails)
    underground_ducts = EmbeddedDocumentField(cableInstallDetails)
    ducts_single = EmbeddedDocumentField(cableInstallDetails)
    ducts_per_cable = EmbeddedDocumentField(cableInstallDetails)
    insulation = EmbeddedDocumentField(cableInsulationDetails)
    sheath = StringField(required=True,
                         choices=cableVar.list_sheathType,
                         default=cableVar.default_sheathType)
    cableScreen = EmbeddedDocumentField(cableScreen)
    coreScreen = EmbeddedDocumentField(coreScreen)
    voltRating = StringField(required=True,
                             choices=cableVar.list_voltRating,
                             default=cableVar.default_voltRating)
    isFlex = StringField(required=True,
                         choices=cableVar.list_flexCable,
                         default=cableVar.default_flexCable)
    armoured = StringField(required=True,
                           choices=cableVar.list_cableArmour,
                           default=cableVar.default_cableArmour)
    impedance = EmbeddedDocumentField(cableImpedance)
    manufacturer = EmbeddedDocumentField(manufacturerDetails)


class cableRun(Document):
    """
    :param tag: TAGS COULD BE A LIST OF TAGS THAT EQUAL IN NUMBER TO THE NUMBER OF CABLES THAT FORM PART OF THE RUN. THIS WOULD ALLEVIATE THE NEED TO SPECIFY EACH CABLES TAG AND ITS ASSOCIATED CABLE TYPE.
    :param cable: THE SPECIFIC CABLES THAT MAKE UP THE RUN ARE REFERENCED WITHIN THE LIST. THE LIST WILL NEED TO ALLOW FOR MORE THAN ONE OF A PARTICULAR cable_id TO BE CONTAINED WITHIN IT. THIS WILL ASSIST WITH THE CONSTRUCTION OF MTOS
    :param cableType:
    :param circuitType:
    :param circuitLength:
    :param numberCables: Number of cables that make up the run. THIS SHOULD BE LINKED TO cables AS DEFINED ABOVE.
    :param CircuitDetail:
    :param currentCapacity: THIS IS THE CABLE RUNS CABLE CARRYING CAPACITY BASED ON THE INSTALLATION METHOD, NUMBER OF PARALLEL CABLES AND THE DERATING FACTOR
    :param installMethod: THIS IS USED TO DETERMINE THE CCC OF THE CABLES IN THE CABLE RUN
    :param loadedTemp: temperature OF THE CABLE RUN BASED ON ACTUAL LOAD AND CABLE SIZE
    :param supply: _id of supplying equipment
    :param load: _id of load equipment
    """
    meta = {'collection': 'CableRun'}
    tag = ListField(required=True)
    cables = ListField(ReferenceField(cableDetails),
                       required=True)
    cableType = StringField(required=True,
                            choices=cableVar.list_cableType)
    circuitType = StringField(choices=cableVar.list_circuitType)
    circuitLength = IntField(required=True,
                             default=0)
    numberCables = IntField(required=True)
    circuitDetail = EmbeddedDocumentField(circuitDetail)
    currentCapacity = IntField(required=True)
    installMethod = StringField(required=True,
                                choices=cableVar.list_installMethod)
    loadedTemp = IntField()
    supply = StringField(required=True)  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
    load = StringField(required=True)  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
    supplyContract = StringField()  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
    installContract = StringField()  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
    connectContract = StringField()  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
    area = StringField()  # THIS SHOULD BE A REFERENCE FIELD EVENTUALLY
    MVAM = DecimalField(precision=4)
    R = DecimalField(precision=4)  # resistance (ohms)
    X = DecimalField(precision=4)  # reactance (ohms)
    Z = DecimalField(precision=4)  # impedance (ohms
    i2t = EmbeddedDocumentField(i2t)
    revision = EmbeddedDocumentField(revisionDetail)

def importCableData(db, filepath):
    """
    Import cable data and add to the database
    """
    import importCSVData as importCSV
    import mongoengine as me

    me.connect(db)
    generator = importCSV.import_data_generator(filepath)
    try:
        for each in generator:
            # print(isinstance(each, object))
            if isinstance(each, dict):
                addcabledict(each)
            else:
                pass

    except Exception as e:
        pass
    finally:
        pass
        # generator.close()

def imporCableRunData():
    """
    """
    pass

def addcabledict(details):
    """
    :param details: cables details contained within a dict.
    """
    cable = cableDetails(description=details["description"])
    cable.conductorMaterial = details["conductorMaterial"]
    cable.cableCoreArrangement = details["coreArrangement"]
    cable.cableType = details["cableType"]
    cable.circuitType = details["circuitType"]
    cable.voltRating = details["voltRating"].upper()
    cable.isFlex = details["isFlex"].title()
    cable.sheath = details["sheath"]
    cable.armoured = details["armoured"]
    # cable.save()
    # if details["unenclosed_spaced.current"]:
    # print("TRUE+++++")
    cable.unenclosed_spaced = cableInstallDetails(
        current=details["unenclosed_spaced.current"],
        installTemp=details["unenclosed_spaced.installTemp"],
        cableArrangement=details["unenclosed_spaced.cableArrangement"]
    )
    # if details["unenclosed_surface.current"]:
    cable.unenclosed_surface = cableInstallDetails(
        current=details["unenclosed_surface.current"],
        installTemp=details["unenclosed_surface.installTemp"],
        cableArrangement=details["unenclosed_surface.cableArrangement"]
    )
    # if details["unenclosed_touching.current"]:
    cable.unenclosed_touching = cableInstallDetails(
        current=details["unenclosed_touching.current"],
        installTemp=details["unenclosed_touching.installTemp"],
        cableArrangement=details["unenclosed_touching.cableArrangement"]
    )
    # if details["enclosed_conduit.current"]:
    cable.enclosed_conduit = cableInstallDetails(
        current=details["enclosed_conduit.current"],
        installTemp=details["enclosed_conduit.installTemp"],
        cableArrangement=details["enclosed_conduit.cableArrangement"]
    )
    # if details["enclosed_partial.current"]:
    cable.enclosed_partial = cableInstallDetails(
        current=details["enclosed_partial.current"],
        installTemp=details["enclosed_partial.installTemp"],
        cableArrangement=details["enclosed_partial.cableArrangement"]
    )
    # if details["enclosed_complete.current"]:
    # print("TRUE----")
    cable.enclosed_complete = cableInstallDetails(
        current=details["enclosed_complete.current"],
        installTemp=details["enclosed_complete.installTemp"],
        cableArrangement=details["enclosed_complete.cableArrangement"]
    )
    # if details["buried_direct.current"]:
    cable.buried_direct = cableInstallDetails(
        current=details["buried_direct.current"],
        installTemp=details["buried_direct.installTemp"],
        cableArrangement=details["buried_direct.cableArrangement"]
    )
    # if details["underground_ducts.current"]:
    cable.underground_ducts = cableInstallDetails(
        current=details["underground_ducts.current"],
        installTemp=details["underground_ducts.installTemp"],
        cableArrangement=details["underground_ducts.cableArrangement"]
    )
    # if details["ducts_single.current"]:
    cable.ducts_single = cableInstallDetails(
        current=details["ducts_single.current"],
        installTemp=details["ducts_single.installTemp"],
        cableArrangement=details["ducts_single.cableArrangement"]
    )
    cable.activeCores = coreDetails(
        size=details["activeCores.size"],
        sizeUnit=details["activeCores.sizeUnit"],
        number=details["activeCores.number"]
    )
    cable.neutralCores = coreDetails(
        size=details["neutralCores.size"],
        sizeUnit=details["neutralCores.sizeUnit"],
        number=details["neutralCores.number"]
    )
    cable.earthCores = coreDetails(
        size=details["earthCores.size"],
        sizeUnit=details["earthCores.sizeUnit"],
        number=details["earthCores.Number"]
    )
    cable.controlCores = coreDetails(
        size=details["controlCores.size"],
        sizeUnit=details["controlCores.sizeUnit"],
        number=details["controlCores.number"]
    )
    cable.instPairs = coreDetails(
        size=details["instPairs.size"],
        sizeUnit=details["instPairs.sizeUnit"],
        number=details["instPairs.number"]
    )
    cable.insulation = cableInsulationDetails(
        name=details["insulation.name"],
        code=details["insulation.code"],
        conductorTemperature=details["insulation.conductorTemperature"],
        maxTemperature=details["insulation.maxTemperature"]
    )
    cable.cableScreen = cableScreen(
        name=details["CableScreen.name"],
        faultWithstand=details["CableScreen.faultWithstand"]
    )
    cable.coreScreen = coreScreen(
        type=details["CoreScreen.type"]
    )
    cable.impedance = cableImpedance(
        MVAM=details["impedance.MVAM"],
        rOhmsPerKM=details["impedance.rOhmsPerKM"],
        xOhmsPerKM=details["impedance.xOhmsPerKM"],
        zOhmsPerKM=details["impedance.zOhmsPerKM"]
    )
    cable.manufacturer = manufacturerDetails(
        name=details["manufacturer.name"],
        partNumber=details["manufacturer.partNumber"]
    )
    cable.save()
