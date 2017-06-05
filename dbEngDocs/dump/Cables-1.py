# coding: utf-8
#
from mongoengine import *
import datetime
import config.cableVariables as cableVar
from functools import reduce

# TODO: Create an exception for cables

# ----------- QUERY SETS


class QueryCableDetails(QuerySet):
    """
    Class to allow the querying of specific cable details.
    if the query parameter is 'DEFAULT' then the query is based on the on the default value for that parameter.
    If query term is 'None' or not in the list of variables, then all values in the list of variables are added to the query.
    """
    def find_cabletype(self, cabletype=None):
        """
        Query based on cable type only.
        :param cabletype:
        :return:
        """
        if (cabletype is not None) and (cabletype.upper() is 'DEFAULT'):
            return self.filter(cableType=cableVar.default_cableType)
        if (cabletype is None) or (cabletype.upper() not in cableVar.list_cableType):
            types = cableVar.list_cableType
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(cableType=code), types))
            return self.filter(query)
        return self.filter(cableType=cabletype.upper())

    def find_circuittype(self, circuittype=None):
        """
        Query based on the circuit type.
        :param circuittype:
        :return:
        """
        if (circuittype is not None) and (circuittype.upper() is 'DEFAULT'):
            return self.filter(circuitType=circuittype.default_circuitType)
        if (circuittype is None) or (circuittype.upper() not in cableVar.list_circuitType):
            types = cableVar.list_circuitType
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(circuitType=code), types))
            return self.filter(query)
        return self.filter(circuitType=circuittype.upper())

    def find_conductormaterial(self, conductor=None):
        """
        Query based on the conductor material.
        :param conductor:
        :return:
        """
        if (conductor is not None) and (conductor.upper() is 'DEFAULT'):
            return self.filter(conductorMaterial=cableVar.default_conductorMaterial)
        if (conductor is None) or (conductor.upper() not in cableVar.list_conductorMaterial):
            material = cableVar.list_conductorMaterial
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(conductorMaterial=code), material))
            return self.filter(query)
        return self.filter(conductorMaterial=conductor.upper())

    def find_cablearrangement(self, arrangement=None):
        """
        Query based on the cable arrangement.
        :param arrangement:
        :return:
        """
        if (arrangement is not None) and (arrangement.upper() is 'DEFAULT'):
            return self.filter(cableArrangement=cableVar.default_cableArrangement)
        if (arrangement is None) or (arrangement.upper() not in cableVar.list_cableArrangement):
            arrangements = cableVar.list_cableArrangement
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(installMethod__cableArrangement=code), arrangements))
            return self.filter(query)
        return self.filter(installMethod__cableArrangement=arrangement.upper())

    def find_insulationtype(self, insulation=None):
        """
        Query based on insulation type.
        :param insulation:
        :return:
        """
        if (insulation is not None) and (insulation.upper() is 'DEFAULT'):
            return self.filter(insulation__name=cableVar.default_insulationType)
        if (insulation is None) or (insulation.upper() not in cableVar.list_insulationType):
            insulationtypes = cableVar.list_insulationType
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(insulation__name=code), insulationtypes))
            return self.filter(query)
        return self.filter(insulation__name=insulation.upper())

    def find_insulationcode(self, insulationcode=None):
        """
        Query based on insulation type.
        :param insulationcode: The insulation code being searched for.
        :return:
        """
        if (insulationcode is not None) and (insulationcode.upper() is 'DEFAULT'):
            return self.filter(insulation__code=cableVar.default_insulationCode)
        if(insulationcode is None) or (insulationcode.upper() not in cableVar.list_insulationCode):
            insulationcodes = cableVar.list_insulationCode
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(insulation__code=code), insulationcodes))
            return self.filter(query)
        return self.filter(insulation__code=insulationcode.upper())

    def find_voltrating(self, volt=None):
        """
        Query based on volt rating.
        :param volt:
        :return:
        """
        if (volt is not None) and (volt.upper() is 'DEFAULT'):
            return self.filter(voltRating=cableVar.default_voltRating)
        if (volt is None) or (volt.upper() not in cableVar.list_voltRating):
            ratings = cableVar.list_voltRating
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(voltRating=code), ratings))
            return self.filter(query)
        return self.filter(voltRating=volt.upper())

    def find_conductorsize(self, size=None):
        """
        Query based on conductor size.
        :param size:
        :return:
        """
        # TODO: Update method to allow conductor to be passed to the method.
        if (size is not None) and (size is 'DEFAULT'):
            return self.filter(activeCores__size__=cableVar.minCableSingleCoreSize)
        if (size is None) or (size < 0):
            return self.filter(activeCores__size__gte=0)
        return self.filter(activeCores__size__=size)

    def find_conductorsizeunit(self, unit=None):
        """
        Query based on size unit.
        :param unit:
        :return:
        """
        # TODO: Update method to allow conductor to be passed to the method.
        if (unit is not None) and (unit.upper() is 'DEFAULT'):
            return self.filter(sizeUnit=cableVar.default_SizeUnit)
        if (unit is None) or (unit not in cableVar.list_sizeUnit):
            unit = cableVar.list_sizeUnit
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(activeCores__sizeUnit=code), unit))
            return self.filter(query)
        return self.filter(activeCores__sizeUnit=unit.upper())

    def find_corearrangement(self, arrangement=None):
        """
        Query based on core arrangement.
        :param arrangement:
        :return:
        """
        if (arrangement is not None) and (arrangement.upper() is 'DEFAULT'):
            return self.filter(coreArrangement=cableVar.default_coreArrangement)
        if (arrangement is None) or (arrangement.upper() not in cableVar.list_coreArrangement):
            arrangements = cableVar.list_coreArrangement
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(coreArrangement=code), arrangements))
            return self.filter(query)
        return self.filter(coreArrangement=arrangement.upper())

    def find_cablearmour(self, armour=None):
        """
        Query based on cable armour.
        :param armour:
        :return:
        """
        if (armour is not None) and (armour.upper() is 'DEFAULT'):
            return self.filter(armoured=cableVar.default_cableArmour)
        if (armour is None) or (armour.upper() not in cableVar.list_cableArmour):
            types = cableVar.list_cableArmour
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(armoured=code), types))
            return self.filter(query)
        return self.filter(armoured=armour.upper())

    def find_cablescreen(self, screen=None):
        """
        Query based on cable screen.
        :param screen:
        :return:
        """
        if (screen is not None) and (screen.upper() is 'DEFAULT'):
            return self.filter(cableScreen__name=cableVar.default_cableScreen)
        if (screen is None) or (screen.upper() not in cableVar.list_cableScreen):
            screens = cableVar.list_cableScreen
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(cableScreen__name=code), screens))
            return self.filter(query)
        return self.filter(cableScreen__name=screen.upper())

    def find_corescreen(self, screen=None):
        """
        Query based on core screen.
        :param screen:
        :return:
        """
        if (screen is not None) and (screen.upper() is 'DEFAULT'):
            return self.filter(coreScreen__name=cableVar.default_coreScreen)
        if (screen is None) or (screen.upper() not in cableVar.list_coreScreen):
            screens = cableVar.list_coreScreen
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(coreScreen__type__=code), screens))
            return self.filter(query)
        return self.filter(coreScreen__type__=screen.upper())

    def find_flexcable(self, flex=None):
        """
        Query based on is flexible cable.
        :param flex:
        :return:
        """
        if (flex is not None) and (flex.upper() is 'DEFAULT'):
            return self.filter(isFlex=cableVar.default_flexCable)
        if (flex is None) or (flex.upper() not in cableVar.list_flexCable):
            types = cableVar.list_flexCable
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(isFlex=code), types))
            return self.filter(query)
        return self.filter(isFlex=flex.upper())

    def find_cablesheath(self, sheath):
        """
        Query based on cable sheath.
        :param sheath:
        :return:
        """
        if (sheath is not None) and (sheath.upper() is 'DEFAULT'):
            return self.filter(sheath=cableVar.default_sheathType)
        if (sheath is None) or (sheath.upper() not in cableVar.list_sheathType):
            types = cableVar.list_sheathType
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(sheath=code), types))
            return self.filter(query)
        return self.filter(sheath=sheath.upper())

    def find_cableinstallmethod(self, install_method=None):
        """
        Query to find cables equal to or greater than the passed current carrying capacity.
        :param install_method:
        :return:
        """
        if (install_method is not None) and (install_method.upper() is 'DEFAULT'):
            return self.filter(installMethod__name=cableVar.default_installMethod)
        if (install_method is None) or (install_method.upper() not in cableVar.list_installMethod):
            methods = cableVar.list_installMethod
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(installMethod__name=code), methods))
            return self.filter(query)
        return self.filter(installMethod__name=install_method)

    def find_cablecurrent_gte(self, installmethod, current):
        """
        Query based on installation method and minimum current carrying capacity.
        :param installmethod:
        :param current:
        :return:
        """
        return self.filter(installMethod__name=installmethod, installMethod__current__gte=current)

    def find_hasneutral(self, hasneutral=True):
        """
        Query based on whether a cable has a neutral conductor or not.
        :param hasneutral:
        :return:
        """
        if hasneutral is True:
            return self.filter(neutralCores__size__gt=0)
        if hasneutral is False:
            return self.filter(neutralCores__size__lte=0)

    def find_query(self, **kwargs):
        """
        A general purpose cable query that allows multiple attributes to be searched at once. The query completes no
        checks on the query and it is up to the user to ensure that the correct attributes are being passed to the query
        and that they are in range.
        :param kwargs:
        :return:
        """
        return self.filter(Q(**kwargs))

    def find_basiccables(self, cabletype=None, loadcurrent=0, conductormaterial=None, voltrating=None, circuittype=None,
                         installmethod=None, mincablesize=None):
        if (cabletype is None) or (cabletype.upper() not in cableVar.list_cableType):
            cabletype = cableVar.default_cableType
        else:
            cabletype = cabletype.upper()
        loadcurrent = loadcurrent
        if (conductormaterial is None) or (conductormaterial.upper() not in cableVar.list_conductorMaterial):
            conductormaterial = cableVar.default_conductorMaterial
        else:
            conductormaterial = conductormaterial.upper()
        if (voltrating is None) or (voltrating.upper() not in cableVar.list_voltRating):
            voltrating = cableVar.default_voltRating
        else:
            voltrating = voltrating.upper()
        if (circuittype is None) or (circuittype.upper() not in cableVar.list_circuitType):
            circuittype = cableVar.default_circuitType
        else:
            circuittype = circuittype.upper()
        if (installmethod is None) or (installmethod.upper() not in cableVar.list_installMethod):
            installmethod = cableVar.default_installMethod
        else:
            installmethod = installmethod.upper()
        if (mincablesize is None) or (mincablesize not in cableVar.list_conductorSize):
            mincablesize = cableVar.default_minCableSize
        else:
            mincablesize = mincablesize
        return self.filter(
            cableType=cabletype,
            installMethod__current__gte=loadcurrent,
            conductorMaterial=conductormaterial,
            voltRating=voltrating,
            circuitType=circuittype,
            installMethod__name=installmethod,
            activeCores__size__=mincablesize
        )


class CoreDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable core.
    It relies on cable variables configuration file being present to check the preferred details.

    size: cross sectional area
    sizeUnit: cross sectional area unit of measure
    number: number of cores
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
        """
        if self.size is '-':
            self.size = 0
        if self.number is '-':
            self.number = 0


class CableInstallMethod(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of the cable installation details.
    It relies on cable variables configuration file being present to check the preferred details.
    :param name:
    :param current: current carrying capacity of the cable
    :param installTemp: the ambient temperature that the current is based on.
    :param cableArrangement: single core cable arrangements.
    """

    name = StringField(
        required=True,
        choices=cableVar.list_installMethod
    )
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
        """
        self.name = self.name.upper()
        self.cableArrangement = self.cableArrangement.upper()


class CableInsulationDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the cable insulation details.
    It relies on cable variables configuration file being present to check the preferred details.
    name:
    conductorTemperature:
    maxTemperature: # maximum conductor temperature. Assumes degrees C
    """
    name = StringField(
        required=True,
        choices=cableVar.list_insulationType,
        default=cableVar.default_insulationType
    )
    conductorTemperature = IntField(
        required=True
    )
    maxTemperature = IntField(
        required=True
    )
    code = StringField(
        required=True,
        choices=cableVar.list_insulationCode,
        default=cableVar.default_insulationCode
    )


class CableScreen(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable screen.
    It relies on cable variables configuration file being present to check the preferred details.

    name: type of screen
    faultWithstand: maximum fault current withstand capability of the screen
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


class CoreScreen(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a core screen.
    It relies on cable variables configuration file being present to check the preferred details.
    type: type of screen
    """
    type = StringField(
        required=True,
        choices=cableVar.list_coreScreen,
        default=cableVar.default_coreScreen
    )

    def clean(self):
        """
        Clean up the provided details.
        """
        self.type = self.type.upper()
        if self.type is 'FALSE':
            self.type = 'NIL'


class CableImpedance(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable impedance details.
    It relies on cable variables configuration file being present to check the preferred details.

    MVAM: Milli-volts per amp-metre
    rOhmsPerKM: resistance (ohms/km)
    xOhmsPerKM: reactance (ohms/km)
    zOhmsPerKM: impedance (ohms/km)
    """
    MVAM = DecimalField(
        precision=4,
        min_value=0
    )
    rOhmsPerKM = DecimalField(
        precision=4,
        min_value=0
    )
    xOhmsPerKM = DecimalField(
        precision=4,
        min_value=0
    )
    zOhmsPerKM = DecimalField(
        precision=4,
        min_value=0
    )


class ManufacturerDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of the manufacturer details.
    It relies on cable variables configuration file being present to check the preferred details.

    name: Manufacturer's name
    partNumber: Manufacturer's part number
    """
    name = StringField()
    partNumber = StringField()


class I2T(EmbeddedDocument):
    #  TODO: Use and application of this class needs to be determined. Should this class be associated with cables or cable runs?
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable I2T details (i.e. associated with fault current withstand capabilities).
    This class doesn't have much in the way of use at the moment and will require additional work.

    kFactor: this will probably have to calculated from a look up table and will be unique to each run
    time: this will be a list of time values ranging from 0.0001 to 5 secs. It can zipped with I2T.current shown below.
    current: this will be a list of current values that be zipped with I2T.time shown above.
    """
    kFactor = IntField(
        required=True
    )
    time = ListField(
        min_value=0.0001,
        max_value=5,
        precision=4
    )
    current = ListField(
        min_value=0
    )


class RevisionDetail(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable's revision details, i.e. when the cable details were updated.
    It relies on cable variables configuration file being present to check the preferred details.

    number: Revision number
    date: date of the most recent change
    """
    number = StringField()
        # required=True

    date = DateTimeField(
        default=datetime.datetime.now()
    )

    def clean(self):
        self.number = self.number.upper()


class CableDetails(Document):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable.
    It relies on cable variables configuration file being present to check the preferred details.

    description: e.g. 3C+E 35mm2 Cu PVC/SWA/PVC 0.6/1kV
    cableType: Describes the type of cable e.g. ACTIVE, EARTH, COMMS etc.
    circuitType: Describes the type of circuit the cable is used for "SINGLE", "MULTI", "CONTROL", "INSTRUMENT" etc.
    conductorMaterial: The material the conductor is made from.
    coreArrangement:
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
    sheath: Details of the cable sheath
    CableScreen: Details of the cable's screen (if any)
    CoreScreen: Details of the cable core's screen (if any)
    voltRating: Maximum voltage rating fo the cable.
    isFlex: Details of how flexiable the cable is.
    armoured: Details of the cable's armouring.
    impedance: Embedded document.
    manufacturer: Details specific to the manufacture of the cable.
    """
    meta = {'collection': 'Cable',
            'queryset_class': QueryCableDetails,
            'ordering': [
                '-conductorMaterial',
                'coreArrangement',
                'activeCores__size',
                'neutralCores_size',
                'earthCores__size',
                'manufacturer__name'
            ]
            }

    activeCores = EmbeddedDocumentField(CoreDetails)
    neutralCores = EmbeddedDocumentField(CoreDetails)
    earthCores = EmbeddedDocumentField(CoreDetails)
    controlCores = EmbeddedDocumentField(CoreDetails)
    instPairs = EmbeddedDocumentField(CoreDetails)
    installMethod = EmbeddedDocumentListField(CableInstallMethod)
    impedance = EmbeddedDocumentField(CableImpedance)
    manufacturer = EmbeddedDocumentField(ManufacturerDetails)
    cableScreen = EmbeddedDocumentField(CableScreen)
    coreScreen = EmbeddedDocumentField(CoreScreen)
    insulation = EmbeddedDocumentField(
        CableInsulationDetails,
        required=True
    )
    sheath = StringField(
        required=True,
        choices=cableVar.list_sheathType,
        default=cableVar.default_sheathType
    )
    # Todo: Should voltRating be an embedded document that allows the phase-earth and phase-phase voltages of the cables to be defined? This would have merit.
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
        RevisionDetail,
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
    coreArrangement = StringField(
        required=True,
        choices=cableVar.list_coreArrangement,
        default=cableVar.default_cableArrangement
    )

    def clean(self):
        """
        Clean up values before importing.
        """
        self.description = self.description.upper()
        self.conductorMaterial = self.conductorMaterial.upper()
        self.coreArrangement = self.coreArrangement.upper()
        if self.coreArrangement is 'NIL':
            self.coreArrangement = "FALSE"
        self.cableType = self.cableType.upper()
        # See what happens here. cableShape isn't a required field
        self.cableShape = self.cableShape.upper()
        self.circuitType = self.circuitType.upper()
        self.voltRating = self.voltRating.upper()
        self.isFlex = self.isFlex.upper()
        if (self.sheath is None) or (self.sheath.upper() not in cableVar.list_sheathType):
            self.sheath = 'UNSHEATHED'
        else:
            self.sheath = self.sheath.upper()
        self.armoured = self.armoured.upper()

    # @queryset_manager
    # def x90(doc_cls, queryset):
    #     # Return cables that
    #     return queryset.filter(activeCores__size__gt=0).order_by(
    #         'conductorMaterial',
    #         'coreArrangement',
    #         'activeCores__size__',
    #         'neutralCores_size__',
    #         'earthCores__size__',
    #     )


# <------- IMPORT FUNCTIONS

def import_cable_data(db, filepath):
    """
    Import cable data and add to the database.
    :param db: MongoDB pointer.
    :param filepath: file path to the CSV file.
    :return:
    """
    # Todo: this should reference an exception at some point.

    import importCSVData as importCSV
    import mongoengine as me

    me.connect(db)
    generator = importCSV.import_data_generator(filepath)
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



def add_cable_dict(details):
    """
    This function is designed for the importation of cables details from a CSV file.

    The function will do some error checking before the MongoEngine's checks. These checks are simple and are intended
    to be basic data entry formatting type checks.

    :param details: cable details contained within a dict.
    """
    cable = CableDetails(description=details["description"])
    cable.conductorMaterial = details["conductorMaterial"]
    if "cableCoreArrangement" in details:
        cable.coreArrangement = details["cableCoreArrangement"]
    else:
        cable.coreArrangement = details["coreArrangement"]
    cable.cableType = details["cableType"]
    if "cableShape" in details:
        cable.cableShape = details["cableShape"]
    cable.circuitType = details["circuitType"]
    cable.voltRating = details["voltRating"]
    cable.isFlex = details["isFlex"]
    cable.sheath = details["sheath"]
    cable.armoured = details["armoured"]
    # for each in cableVar.list_installMethod:
    #     try:
    #         cable.installMethod[each.lower()] = CableInstallMethod(
    #             # name=each.lower(),
    #             current=details[str(each.lower())+'.current'],
    #             installTemp=details[str(each.lower()) + '.installTemp'],
    #             cableArrangement=details[str(each.lower()) + '.cableArrangement']
    #         )
    #         # cable.installMethod.append(installation)
    #     except Exception as e:
    #         print(e)

    for each in cableVar.list_installMethod:
        try:
            installation = CableInstallMethod(
                name=each.lower(),
                current=details[str(each.lower()) + '.current'],
                installTemp=details[str(each.lower()) + '.installTemp'],
                cableArrangement=details[str(each.lower()) + '.cableArrangement']
            )
            cable.installMethod.append(installation)
        except Exception as e:
            print(e)


    # if "unenclosed_spaced.current" in details:
    #     cable.unenclosed_spaced = CableInstallDetails(
    #         current=details["unenclosed_spaced.current"],
    #         installTemp=details["unenclosed_spaced.installTemp"],
    #         cableArrangement=details["unenclosed_spaced.cableArrangement"]
    #     )
    # if "unenclosed_surface.current" in details:
    #     cable.unenclosed_surface = CableInstallDetails(
    #         current=details["unenclosed_surface.current"],
    #         installTemp=details["unenclosed_surface.installTemp"],
    #         cableArrangement=details["unenclosed_surface.cableArrangement"]
    #     )
    # if "unenclosed_touching.current" in details:
    #     cable.unenclosed_touching = CableInstallDetails(
    #         current=details["unenclosed_touching.current"],
    #         installTemp=details["unenclosed_touching.installTemp"],
    #         cableArrangement=details["unenclosed_touching.cableArrangement"]
    #     )
    # if "enclosed_conduit.current" in details:
    #     cable.enclosed_conduit = CableInstallDetails(
    #         current=details["enclosed_conduit.current"],
    #         installTemp=details["enclosed_conduit.installTemp"],
    #         cableArrangement=details["enclosed_conduit.cableArrangement"]
    #     )
    # if "enclosed_partial.current" in details:
    #     cable.enclosed_partial = CableInstallDetails(
    #         current=details["enclosed_partial.current"],
    #         installTemp=details["enclosed_partial.installTemp"],
    #         cableArrangement=details["enclosed_partial.cableArrangement"]
    #     )
    # if "enclosed_complete.current" in details:
    #     cable.enclosed_complete = CableInstallDetails(
    #         current=details["enclosed_complete.current"],
    #         installTemp=details["enclosed_complete.installTemp"],
    #         cableArrangement=details["enclosed_complete.cableArrangement"]
    #     )
    # if "unenclosed_partial.current" in details:
    #     cable.unenclosed_partial = CableInstallDetails(
    #         current=details["unenclosed_partial.current"],
    #         installTemp=details["unenclosed_partial.installTemp"],
    #         cableArrangement=details["unenclosed_partial.cableArrangement"]
    #     )
    # if "unenclosed_complete.current" in details:
    #     cable.unenclosed_complete = CableInstallDetails(
    #         current=details["unenclosed_complete.current"],
    #         installTemp=details["unenclosed_complete.installTemp"],
    #         cableArrangement=details["unenclosed_complete.cableArrangement"]
    #     )
    # if "buried_direct.current" in details:
    #     cable.buried_direct = CableInstallDetails(
    #         current=details["buried_direct.current"],
    #         installTemp=details["buried_direct.installTemp"],
    #         cableArrangement=details["buried_direct.cableArrangement"]
    #     )
    # if "underground_ducts.current" in details:
    #     cable.underground_ducts = CableInstallDetails(
    #         current=details["underground_ducts.current"],
    #         installTemp=details["underground_ducts.installTemp"],
    #         cableArrangement=details["underground_ducts.cableArrangement"]
    #     )
    # if "ducts_single.current" in details:
    #     cable.ducts_single = CableInstallDetails(
    #         current=details["ducts_single.current"],
    #         installTemp=details["ducts_single.installTemp"],
    #         cableArrangement=details["ducts_single.cableArrangement"]
    #     )
    # if "ducts_per_cable.current" in details:
    #     cable.ducts_per_cable = CableInstallDetails(
    #         current=details["ducts_per_cable.current"],
    #         installTemp=details["ducts_per_cable.installTemp"],
    #         cableArrangement=details["ducts_per_cable.cableArrangement"]
    #     )
    if "activeCores.size" in details:
        cable.activeCores = CoreDetails(
            size=details["activeCores.size"],
            sizeUnit=details["activeCores.sizeUnit"],
            number=details["activeCores.number"]
        )
    if "neutralCores.size" in details:
        cable.neutralCores = CoreDetails(
             size=details["neutralCores.size"],
            sizeUnit=details["neutralCores.sizeUnit"],
            number=details["neutralCores.number"]
        )
    if "earthCores.size" in details:
        cable.earthCores = CoreDetails(
            size=details["earthCores.size"],
            sizeUnit=details["earthCores.sizeUnit"],
            number=details["earthCores.number"]
        )
    if "controlCores.size" in details:
        cable.controlCores = CoreDetails(
            size=details["controlCores.size"],
            sizeUnit=details["controlCores.sizeUnit"],
            number=details["activeCores.number"]
        )
    if "instPairs.size" in details:
        cable.instPairs = CoreDetails(
            size=details["instPairs.size"],
            sizeUnit=details["instPairs.sizeUnit"],
            number=details["instPairs.number"]
        )
    cable.insulation = CableInsulationDetails(
        name=details["insulation.name"],
        code=details["insulation.code"],
        conductorTemperature=details["insulation.conductorTemperature"],
        maxTemperature=details["insulation.maxTemperature"]
    )
    if "CableScreen.name" in details:
        cable.cableScreen = CableScreen(
            name=details["CableScreen.name"],
            faultWithstand=details["CableScreen.faultWithstand"]
        )

    if "CoreScreen.type" in details:
        cable.coreScreen = CoreScreen(
            type=details["CoreScreen.type"]
        )

    cable.impedance = CableImpedance(
        MVAM=details["impedance.MVAM"],
        rOhmsPerKM=details["impedance.rOhmsPerKM"],
        xOhmsPerKM=details["impedance.xOhmsPerKM"],
        zOhmsPerKM=details["impedance.zOhmsPerKM"]
    )
    cable.manufacturer = ManufacturerDetails(
        name=details["manufacturer.name"],
        partNumber=details["manufacturer.partNumber"]
    )
    cable.rev = RevisionDetail(
        number=details["rev.number"],
        date=datetime.datetime.now()
    )
    cable.save()

    def selectcables(cabletype=None, loadcurrent=0, conductormaterial=None, insulationtype=None, insulationcode=None, sheath=None, circuitvoltage=None,
                     armour=None, cablescreen=None, corescreen=None, flexible=False, cores=None, circuittype=None,
                     installationmethod=None, cableshape=None, neutralrequired=True, manufacturer=None):
        """
        :param loadcurrent:
        :param conductormaterial:
        :param insulationtype:
        :param insulationcode:
        :param sheath:
        :param circuitvoltage:
        :param armour: True/False/Any
        :param manufacturer:
        :param cablescreen:
        :param corescreen:
        :param flexible: True/False/Any
        :param cores:
        :param circuittype:
        :param installationmethod:
        :param cableshape:
        :param neutralrequired: True/False/Any
        Find cables that meet the cable run's requirements.
        0. The circuit requirements to this function
        1. Pass required details to Cables.findcable() → this should return a generator object.
        2. Calculate volt drop
        3. Calculate earth fault loop impedance.
        4. Select additional earth conductor if required.
        :return:
        """
        if circuittype is not None:
            circuittype = circuittype.upper()
        else:
            circuittype = circuittype
        loadcurrent = loadcurrent
        if conductormaterial is not None:
            conductormaterial = conductormaterial.upper()
        else:
            conductormaterial = conductormaterial
        if insulationtype is not None:
            insulationtype = insulationtype.upper()
        else:
            insulationtype = insulationtype
        if insulationcode is not None:
            insulationcode = insulationcode.upper()
        else:
            insulationcode = insulationcode
        if sheath is not None:
            sheath = sheath.upper()
        else:
            sheath = sheath
        circuitvoltage = circuitvoltage
        if armour is not None:
            armour = armour.upper()
        else:
            armour = armour
        if cablescreen is not None:
            cablescreen = cablescreen.upper()
        else:
            cablescreen = cablescreen
        if corescreen is not None:
            corescreen = corescreen.upper()
        else:
            corescreen = corescreen
        flexible = flexible
        if cores is not None:
            cores = cores.upper()
        else:
            cores = cores
        if circuittype is not None:
            circuittype = circuittype.upper()
        else:
            circuittype = circuittype
        if installationmethod is not None:
            installationmethod = installationmethod.upper()
        else:
            installationmethod = installationmethod
        if cableshape is not None:
            cableshape = cableshape.upper()
        else:
            cableshape = cableshape
        neutralrequired = neutralrequired
        if manufacturer is not None:
            manufacturer = manufacturer.upper()
        else:
            manufacturer = manufacturer

        return CableDetails.object().find_cable_type(circuittype).find_cable_current_gte(installationmethod, loadcurrent).find_cable_conductor_material(conductormaterial).find_insulation_type(insulationtype).find_insulation_code(insulationcode).find_cable_sheat(sheath)


def cable_search_generator(cabletype='DEFAULT',
        loadcurrent=0,
        conductormaterial='DEFAULT',
        voltrating='DEFAULT',
        circuittype='DEFAULT',
        installmethod='DEFAULT',
        mincablesize=None, **kwargs):
    """
    Complete a basic query on the Cables collection and return a generator using the returned cables.
    :param cabletype:
    :param loadcurrent:
    :param conductormaterial:
    :param voltrating:
    :param circuittype:
    :param installmethod:
    :parma mincablesize:
    :param kwargs:
    :return:
    """
    cables = Cables.CableDetails.objects.find_basiccables(
        cabletype=cabletype, loadcurrent=loadcurrent,
        conductormaterial=conductormaterial,
        voltrating=voltrating, circuittype=circuittype,
        installmethod=installmethod,
        mincablesize=mincablesize)
    yield cables

        # def findcable(cabletype=None, minCCC=0, circuittype=None, installmethod=None, conductormaterial=None, insulation=None, sheath=None, corearrangement=None, voltrating=None, armour=None, neutral=True):
#     """
#     DB query to find a cable based on the parameters.
#     :param cabletype: define the cable type as per list_cableType.
#     :param minCCC: the minimum current carrying capacity of the cable.
#     :param circuittype: circuit type as per list_circuitType.
#     :param installmethod: cable installation method as per the
#     :param conductormaterial: material the conductor is manufactured from.
#     :param insulation: Cable insulation
#     :param sheath: material the cable sheath is made from.
#     :param corearrangement: single core cable arrangement.
#     :param voltrating: cable insulation voltage capacity
#     :param armour: is the cable armoured
#     :param neutral: does the cable require a neutral conductor?
#     :return: objects found by the search
#     """
#     # Set the search for a particular cable type in the database.
#     # This will be used to determine the core type being searched.
#     if cabletype is not None:
#         cableType = cabletype.upper()
#
#     current = minCCC
#
#     if circuittype is not None:
#         circuitType = circuittype.upper()
#
#     if corearrangement is not None:
#         coreArrengemnt = corearrangement.upper()
#
#
#     if installmethod is not None:
#         pass
#
#     if conductormaterial is not None:
#         pass
#     if insulation is not None:
#         pass
#     if sheath is not None:
#         pass
#     if corearrangement is not None:
#         pass
#     if voltrating is not None:
#         pass
#     if armour is not None:
#         pass
#
#     return Cables.Cable.object()