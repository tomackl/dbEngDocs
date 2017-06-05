# coding: utf-8
#
from mongoengine import *
#import pymongo
import datetime
import config.cableVariables as cableVar

# <----- IMPORT FUNCTION MONGO ENGINE DETAILS

class coreDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable core.
    It relies on cable variables configuration file being present to check the preferred details.

    :param size: cross sectional area
    :param sizeUnit: cross sectional area unit of measure
    :param number: number of cores
    """
    size = DecimalField(precision=1,
                        choices=cableVar.list_conductorSize,
                        default=cableVar.default_minCableSize)
    sizeUnit = StringField(choices=cableVar.list_sizeUnit,
                           default=cableVar.default_SizeUnit)
    number = IntField(min_value=0)

    def clean(self):
        """
        Clean up the data provided.
        :return:
        """
        if self.size is '-':
            self.size = 0
        if self.number is '-':
            self.number = 0


class cableInstallDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of the cable installation details.
    It relies on cable variables configuration file being present to check the preferred details.

    :param current: current carrying capacity of the cable
    :param installTemp: the ambient temperature that the current is based on.
    :param cableArrangement: single core cable arrangements.
    """
    current = IntField(
        required=True,
        min_value=0
    )
    installTemp = IntField(
        required=True,
        min_value=0
    )
    cableArrangement = StringField(
        choices=cableVar.list_cableArrangement,
        required=True
    )

    def clean(self):
        """
        Clean the provided values.
        :return:
        """
        self.cableArrangement = self.cableArrangement.upper()


class cableInsulationDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the cable insulation details.
    It relies on cable variables configuration file being present to check the preferred details.
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
    Mongo Engine data checking class.
    This class defines and checks the details of a cable screen.
    It relies on cable variables configuration file being present to check the preferred details.

    :param name: type of screen
    :param faultWithstand: maximum fault current withstand capability of the screen
    """
    # TODO: CHECK WHETHER FAULT WITHSTAND SHOULD BE ASSIGNED TO CORE SCREEN

    name = StringField(
        choices=cableVar.list_cableScreen,
        default=cableVar.default_cableScreen
    )
    faultWithstand = IntField(min_value=0)

    def clean(self):
        """
        Clean up the provided details.
        :return:
        """
        self.name = self.name.upper()


class coreScreen(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a core screen.
    It relies on cable variables configuration file being present to check the preferred details.
    :param type: type of screen
    """
    type = StringField(
        required=True,
        choices=cableVar.list_coreScreen,
        default=cableVar.default_coreScreen
    )

    def clean(self):
        """
        Clean up the provided details.
        :return:
        """
        self.type = self.type.upper()
        if self.type is 'FALSE':
            self.type = 'NIL'


class cableImpedance(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable impedance details.
    It relies on cable variables configuration file being present to check the preferred details.

    :param MVAM: Milli-volts per amp-metre
    :param rOhmsPerKM: resistance (ohms/km)
    :param xOhmsPerKM: reactance (ohms/km)
    :param zOhmsPerKM: impedance (ohms/km)
    """
    MVAM = DecimalField(precision=4, min_value=0)
    rOhmsPerKM = DecimalField(precision=4, min_value=0)
    xOhmsPerKM = DecimalField(precision=4, min_value=0)
    zOhmsPerKM = DecimalField(precision=4, min_value=0)


class manufacturerDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of the manufacturer details.
    It relies on cable variables configuration file being present to check the preferred details.

    :param name: Manufacturer's name
    :param partNumber: Manufacturer's part number
    """
    name = StringField()
    partNumber = StringField()


class i2t(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable I2T details (i.e. associated with fault current withstand capabilities).
    This class doesn't have much in the way of use at the moment and will require additional work.

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
    Mongo Engine data checking class.
    This class defines and checks the details of a cable's revision details, i.e. when the cable details were updated.
    It relies on cable variables configuration file being present to check the preferred details.

    :param number: Revision number
    :param date: date of the most recent change
    """
    number = StringField()
        # required=True

    date = DateTimeField(
        default=datetime.datetime.now()
    )


class circuitDetail(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of circuits that the cable is associated with.
    It relies on cable variables configuration file being present to check the preferred details.

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
    deratingFactor = FloatField(default=1,
                                min_value=0)


class cableDetails(Document):
    """
    Mongo Engine data checking class.
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
    meta = {'collection': 'Cable'}

    activeCores = EmbeddedDocumentField(coreDetails)
    neutralCores = EmbeddedDocumentField(coreDetails)
    earthCores = EmbeddedDocumentField(coreDetails)
    controlCores = EmbeddedDocumentField(coreDetails)
    instPairs = EmbeddedDocumentField(coreDetails)
    unenclosed_spaced = EmbeddedDocumentField(cableInstallDetails)
    unenclosed_surface = EmbeddedDocumentField(cableInstallDetails)
    unenclosed_touching = EmbeddedDocumentField(cableInstallDetails)
    enclosed_conduit = EmbeddedDocumentField(cableInstallDetails)
    enclosed_partial = EmbeddedDocumentField(cableInstallDetails)
    enclosed_complete = EmbeddedDocumentField(cableInstallDetails)
    unenclosed_partial = EmbeddedDocumentField(cableInstallDetails)
    unenclosed_complete = EmbeddedDocumentField(cableInstallDetails)
    buried_direct = EmbeddedDocumentField(cableInstallDetails)
    underground_ducts = EmbeddedDocumentField(cableInstallDetails)
    ducts_single = EmbeddedDocumentField(cableInstallDetails)
    ducts_per_cable = EmbeddedDocumentField(cableInstallDetails)
    impedance = EmbeddedDocumentField(cableImpedance)
    manufacturer = EmbeddedDocumentField(manufacturerDetails)
    cableScreen = EmbeddedDocumentField(cableScreen)
    coreScreen = EmbeddedDocumentField(coreScreen)
    insulation = EmbeddedDocumentField(
        cableInsulationDetails,
        required=True
    )
    sheath = StringField(
        required=True,
        choices=cableVar.list_sheathType,
        default=cableVar.default_sheathType
    )
    voltRating = StringField(
        required=True,
        choices=cableVar.list_voltRating,
        default=cableVar.default_voltRating
    )
    isFlex = StringField(
        required=True,
        choices=cableVar.list_flexCable,
        default=cableVar.default_flexCable
    )
    armoured = StringField(
        required=True,
        choices=cableVar.list_cableArmour,
        default=cableVar.default_cableArmour
    )
    rev = EmbeddedDocumentField(
        revisionDetail,
        required=True
    )
    description = StringField(  # e.g. 3C+E 35mm2 Cu PVC/SWA/PVC 0.6/1kV
        required=True
    )
    cableType = StringField(
        required=True,
        choices=cableVar.list_cableType,
        default='-'
        # cableVar.default_cableType
    )
    circuitType = StringField(
        required=True,
        choices=cableVar.list_circuitType
    )
    cableShape = StringField(
        required=True,
        choices=cableVar.list_cableShape,
        default=cableVar.default_cableShape
    )
    conductorMaterial = StringField(
        required=True,
        choices=cableVar.list_conductorMaterial,
        default=cableVar.default_conductorMaterial
    )
    cableCoreArrangement = StringField(
        required=True,
        choices=cableVar.list_coreArrangements,
        default=cableVar.default_cableArrangement
    )

    def clean(self):
        """
        Clean up values before importing.
        :return:
        """
        self.description = self.description.upper()
        self.conductorMaterial = self.conductorMaterial.upper()
        self.cableCoreArrangement = self.cableCoreArrangement.upper()
        if self.cableCoreArrangement is 'NIL':
            self.cableCoreArrangement = "FALSE"
        self.cableType = self.cableType.upper()
        # See what happens here. cableShape isn't a required field
        self.cableShape = self.cableShape.upper()
        self.circuitType = self.circuitType.upper()
        self.voltRating = self.voltRating.upper()
        self.isFlex = self.isFlex.upper()
        self.sheath = self.sheath.upper()
        self.armoured = self.armoured.upper()



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
    cables = ListField(ReferenceField(cableDetails))
                       # required=True)
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


# <------- IMPORT FUNCTIONS

def importCableData(db, filepath):
    """
    Import cable data and add to the database.
    """
    import importCSVData as importCSV
    import mongoengine as me

    me.connect(db)
    generator = importCSV.import_data_generator(filepath)
    try:
        for each in generator:
            if isinstance(each, dict):
                addcabledict(each)
            else:
                print("NOT A DICT!!")

    except Exception as e:
        print(e)
    finally:
        generator.close()


def importCableRunData():
    """
    """
    pass


def addcabledict(details):
    """
    This function is designed for the importation of cables details from a CSV file.

    The function will do some error checking before the MongoEngine's checks. These checks are simple and are intended to be basic data entry formating type checks.

    :param details: cables details contained within a dict.
    """
    cable = cableDetails(description=details["description"])
    # cable = CableDetails(description=details["description"].upper())
    # cable._id = 1
    cable.conductorMaterial = details["conductorMaterial"]
    cable.cableCoreArrangement = details["coreArrangement"]
    # if details["coreArrangement"].upper() is "FALSE":
    #     cable.coreArrangement = "NIL"
    # else:
    #     cable.coreArrangement = details["coreArrangement"].upper()
    cable.cableType = details["cableType"]
    # cable.cableType = details["cableType"].upper()
    if "cableShape" in details:
        cable.cableShape = details["cableShape"]
        # cable.cableShape = details["cableShape"].upper()
    cable.circuitType = details["circuitType"]
    # cable.circuitType = details["circuitType"].upper()
    cable.voltRating = details["voltRating"]
    cable.isFlex = details["isFlex"]
    cable.sheath = details["sheath"]
    # cable.voltRating = details["voltRating"].upper()
    # cable.isFlex = details["isFlex"].upper()
    # cable.sheath = details["sheath"].upper()
    cable.armoured = details["armoured"]
    # TODO: Find a way of turning the below into a function/method
    if "unenclosed_spaced.current" in details:
        cable.unenclosed_spaced = cableInstallDetails(
            current=details["unenclosed_spaced.current"],
            installTemp=details["unenclosed_spaced.installTemp"],
            cableArrangement=details["unenclosed_spaced.cableArrangement"]
        )
    if "unenclosed_surface.current" in details:
        cable.unenclosed_surface = cableInstallDetails(
            current=details["unenclosed_surface.current"],
            installTemp=details["unenclosed_surface.installTemp"],
            cableArrangement=details["unenclosed_surface.cableArrangement"]
        )
    if "unenclosed_touching.current" in details:
        cable.unenclosed_touching = cableInstallDetails(
            current=details["unenclosed_touching.current"],
            installTemp=details["unenclosed_touching.installTemp"],
            cableArrangement=details["unenclosed_touching.cableArrangement"]
        )
    if "enclosed_conduit.current" in details:
        cable.enclosed_conduit = cableInstallDetails(
            current=details["enclosed_conduit.current"],
            installTemp=details["enclosed_conduit.installTemp"],
            cableArrangement=details["enclosed_conduit.cableArrangement"]
        )
    if "enclosed_partial.current" in details:
        cable.enclosed_partial = cableInstallDetails(
            current=details["enclosed_partial.current"],
            installTemp=details["enclosed_partial.installTemp"],
            cableArrangement=details["enclosed_partial.cableArrangement"]
        )
    if "enclosed_complete.current" in details:
        cable.enclosed_complete = cableInstallDetails(
            current=details["enclosed_complete.current"],
            installTemp=details["enclosed_complete.installTemp"],
            cableArrangement=details["enclosed_complete.cableArrangement"]
        )
    if "unenclosed_partial.current" in details:
        cable.unenclosed_partial = cableInstallDetails(
            current=details["unenclosed_partial.current"],
            installTemp=details["unenclosed_partial.installTemp"],
            cableArrangement=details["unenclosed_partial.cableArrangement"]
        )
    if "unenclosed_complete.current" in details:
        cable.unenclosed_complete = cableInstallDetails(
            current=details["unenclosed_complete.current"],
            installTemp=details["unenclosed_complete.installTemp"],
            cableArrangement=details["unenclosed_complete.cableArrangement"]
        )
    if "buried_direct.current" in details:
        cable.buried_direct = cableInstallDetails(
            current=details["buried_direct.current"],
            installTemp=details["buried_direct.installTemp"],
            cableArrangement=details["buried_direct.cableArrangement"]
        )
    if "underground_ducts.current" in details:
        cable.underground_ducts = cableInstallDetails(
            current=details["underground_ducts.current"],
            installTemp=details["underground_ducts.installTemp"],
            cableArrangement=details["underground_ducts.cableArrangement"]
        )
    if "ducts_single.current" in details:
        cable.ducts_single = cableInstallDetails(
            current=details["ducts_single.current"],
            installTemp=details["ducts_single.installTemp"],
            cableArrangement=details["ducts_single.cableArrangement"]
        )
    if "ducts_per_cable.current" in details:
        cable.ducts_per_cable = cableInstallDetails(
            current=details["ducts_per_cable.current"],
            installTemp=details["ducts_per_cable.installTemp"],
            cableArrangement=details["ducts_per_cable.cableArrangement"]
        )
    if "activeCores.size" in details:
        # if details["activeCores.size"] is '-':
        #     coresize = 0
        # else:
        #     coresize = details["activeCores.size"]
        # if details["activeCores.number"] is '-':
        #     corenumber = 0
        # else:
        #     corenumber = details["activeCores.number"]
        cable.activeCores = coreDetails(
            # size=coresize,
            size=details["activeCores.size"],
            sizeUnit=details["activeCores.sizeUnit"],
            # number=corenumber
            number=details["activeCores.number"]
        )
    if "neutralCores.size" in details:
        # if details["neutralCores.size"] is '-':
        #     coresize = 0
        # else:
        #     coresize = details["neutralCores.size"]
        # if details["neutralCores.number"] is '-':
        #     corenumber = 0
        # else:
        #     corenumber = details["neutralCores.number"]
        cable.neutralCores = coreDetails(
            # size=coresize,
            size=details["neutralCores.size"],
            sizeUnit=details["neutralCores.sizeUnit"],
            # number=corenumber
            number = details["neutralCores.number"]
        )
    # print("{}".format(details["earthCores.number"]))
    if "earthCores.size" in details:
        # if details["earthCores.size"] is '-':
        #     coresize = 0
        # else:
        #     coresize = details["earthCores.size"]
        # if details["earthCores.number"] is '-':
        #     corenumber = 0
        # else:
        #     corenumber = details["earthCores.number"]
        cable.earthCores = coreDetails(
            # size=coresize,
            size=details["earthCores.size"],
            sizeUnit=details["earthCores.sizeUnit"],
            # number=corenumber
            number=details["earthCores.number"]
        )
    if "controlCores.size" in details:
        # if details["controlCores.size"] is '-':
        #     coresize = 0
        # else:
        #     coresize = details["controlCores.size"]
        # if details["controlCores.number"] is '-':
        #     corenumber = 0
        # else:
        #     corenumber = details["activeCores.number"]
        cable.controlCores = coreDetails(
            # size=coresize,
            size=details["controlCores.size"],
            sizeUnit=details["controlCores.sizeUnit"],
            # number=corenumber
            number=details["activeCores.number"]
        )
    if "instPairs.size" in details:
        # if details["instPairs.size"] is '-':
        #     coresize = 0
        # else:
        #     coresize = details["instPairs.size"]
        # if details["instPairs.number"] is '-':
        #     corenumber = 0
        # else:
        #     corenumber = details["instPairs.number"]
        cable.instPairs = coreDetails(
            # size=coresize,
            size=details["instPairs.size"],
            sizeUnit=details["instPairs.sizeUnit"],
            # number=corenumber
            number=details["instPairs.number"]
        )
    cable.insulation = cableInsulationDetails(
        name=details["insulation.name"],
        code=details["insulation.code"],
        conductorTemperature=details["insulation.conductorTemperature"],
        maxTemperature=details["insulation.maxTemperature"]
    )
    if "CableScreen.name" in details:
        # if details["CableScreen.name"].upper() in cableVar.list_cableScreen:
        #     cablescreenname = details["CableScreen.name"].upper()
        # if details["CableScreen.name"] not in cableVar.list_cableScreen:
        #     cablescreenname = 'NIL'
        cable.cableScreen = cableScreen(
            # name=cablescreenname,
            name=details["CableScreen.name"],
            faultWithstand=details["CableScreen.faultWithstand"]
        )

    if "CoreScreen.type" in details:
        # if details["CoreScreen.type"].upper() in cableVar.list_coreScreen:
        #     cable.CoreScreen = CoreScreen(
        #         type=details["CoreScreen.type"].upper()
        #     )
        # elif details["CoreScreen.type"].upper() is "FALSE":
        #     cable.CoreScreen = CoreScreen(
        #         type="NIL"
        #     )
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
    cable.rev = revisionDetail(
        number=details["rev.number"],
        date=datetime.datetime.now()
    )
    cable.save()


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