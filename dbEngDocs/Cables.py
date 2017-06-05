# coding: utf-8
#
from mongoengine import *
import datetime
import config.cableVariables as cableVar
from functools import reduce

# TODO: Create an exception for cables

# ----------- QUERY SETS


class QueryCable(QuerySet):
    """
    Class to allow the querying of specific cable details.
    if the query parameter is 'DEFAULT' then the query is based on the on the default value for that parameter.
    If query term is 'None' or not in the list of variables, then all values in the list of variables are added to the query.
    """

    # TODO: add controlCores query
    # TODO: add instPairs query
    # TODO: impedance query : Do we want this?
    # TODO: Find cable larger than minimum size and in order

    def sort_activesize(self):
        """
        Query to sort by the active cable core size.
        :return:
        """
        return self.order_by('activeCores')

    def sort_neutralsize(self):
        """
        Query to sort by the neutral cable core size.
        :return:
        """
        return self.order_by('neutralCores')

    def sort_earthsize(self):
        """
        Query to sort by the earth cable core size.
        :return:
        """
        return self.order_by('earthCores')

    def sort_corearrangement(self, order='DESCEND'):
        """
        Query to sort by cable core arangement.
        :return:
        """
        if order.upper() == 'ASCEND':
            return self.order_by('+coreArrangement')
        if order.upper() == 'DESCEND':
            return self.order_by('-coreArrangement')

    def sort_conductormaterial(self):
        """
        Query to sort by the cable conductor material.
        :return:
        """
        return self.order_by('conductorMaterial')

    def find_manufacturername(self, manufacturer):
        """
        Query to find cable manufacturer.
        :param manufacturer:
        :return:
        """
        # TODO: Update query to search for manufacturer
        return self.filter(manufacturer__name=manufacturer.upper())

    def find_partnumber(self, part):
        """
        Query to find cable manufacturer.
        :param part:
        :return:
        """
        return self.filter(manufacturer__partnumber=part.upper())

    def find_specificcable(self, id):
        """
        Query the database to find a specific cable based on its object_id.
        :param id:
        :return:
        """
        return self.filter(id=id)

    def find_cabletype(self, cabletype=None):
        """
        Query based on cable type only.
        :param cabletype:
        :return:
        """
        if (cabletype is not None) and (cabletype.upper() == 'DEFAULT'):
            return self.filter(cableType=cableVar.default_cableType)
        if (cabletype is None) or (cabletype.upper() not in cableVar.list_cableType):
            types = cableVar.list_cableType
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(cableType=code), types))
            return self.filter(query)
        return self.filter(cableType=cabletype.upper())

    def find_cablesheath(self, cablesheath=None):
        """
        Query based on cable sheath only.
        :param cablesheath:
        :return:
        """
        if (cablesheath is not None) and (cablesheath.upper() == 'DEFAULT'):
            return self.filter(sheath=cableVar.default_sheathType)
        if (cablesheath is None) or (cablesheath.upper() not in cableVar.list_sheathType):
            types = cableVar.list_sheathType
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(sheath=code), types))
            return self.filter(query)
        return self.filter(sheath=cablesheath.upper())

    def find_circuittype(self, circuittype=None):
        """
        Query based on the circuit type.
        :param circuittype:
        :return:
        """
        if (circuittype is not None) and (circuittype.upper() == 'DEFAULT'):
            return self.filter(circuitType=cableVar.default_circuitType)
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
        if (conductor is not None) and (conductor.upper() == 'DEFAULT'):
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
        if (arrangement is not None) and (arrangement.upper() == 'DEFAULT'):
            return self.filter(cableArrangement=cableVar.default_cableArrangement)
        if (arrangement is None) or (arrangement.upper() not in cableVar.list_cableArrangement):
            arrangements = cableVar.list_cableArrangement
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(installMethod__cableArrangement__=code), arrangements))
            return self.filter(query)
        return self.filter(installMethod__cableArrangement__=arrangement.upper())

    def find_insulationtype(self, insulation=None):
        """
        Query based on insulation type.
        :param insulation:
        :return:
        """
        if (insulation is not None) and (insulation.upper() == 'DEFAULT'):
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

    def find_cableshape(self, shape=None):
        """
        Query based on volt rating.
        :param shape:
        :return:
        """
        if (shape is not None) and (shape.upper() is 'DEFAULT'):
            return self.filter(cableShape=cableVar.default_cableShape)
        if (shape is None) or (shape.upper() not in cableVar.list_cableShape):
            ratings = cableVar.list_cableShape
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(
                               cableShape=code),
                               ratings)
                           )
            return self.filter(query)
        return self.filter(cableShape=shape.upper())

    def find_conductorsizerange(self, arrangement, min_size, max_size):
        """
        Query to find conductors based on an arrangement and between certain sizes. This query expects that lists will be passed to it. The value contained in the lists passed to the query are expected to be passed in order.
        :param arrangement: list of core arrangements.
        :param min_size: list of minimum conductor size
        :param max_size: list of maximum conductor size.
        :return:
        """
        arrangement = arrangement
        min_size = min_size
        max_size = max_size
        query = reduce(lambda q1, q2: q1.__or__(q2),
                       map(lambda arrangement, min_size, max_size:
                           Q(coreArrangement=arrangement,
                             activeCores__size__gte=min_size,
                             activeCores__size__lte=max_size),
                           arrangement, min_size, max_size
                           )
                       )
        return self.filter(query)

    def find_conductorsize(self, size=None, coretype='ACTIVE'):
        """
        Query based on conductor size. The query will default to the minimum cable size defined within cableVar.py,
        except for earth cables which will default to 0.
        :param size: cross sectional area of the cable being queried.
        :param coretype: whether the core is an active, neutral or earth cable. Default to 'ACTIVE'.
        :return:
        """

        if coretype.upper() == 'ACTIVE':
            if (size is not None) and (size == 'DEFAULT'):
                return self.filter(activeCores__size__gte=cableVar.default_minCableSize)
            if (size is None) or (size < 0):
                return self.filter(activeCores__size__gte=0)
            return self.filter(activeCores__size__gte=size)

        if coretype.upper() == 'NEUTRAL':
            if (size is not None) and (size == 'DEFAULT'):
                return self.filter(neutralCores__size__=cableVar.default_minCableSize)
            if (size is None) or (size < 0):
                return self.filter(neutralCores__size__gte=0)
            return self.filter(neutralCores__size__=size)

        # Do not apply a minimum earth conductor size
        if coretype.upper() == 'EARTH':
            if (size is None) or (size < 0) or (size == 'DEFAULT'):
                return self.filter(earthCores__size__gte=0)
            return self.filter(earthCores__size__=size)

    def find_maxconductorsize(self, size=None, coretype='ACTIVE'):
        """
        Query based on a maximum conductor size. The query will return a maximum cable size based, that defaults to the
        size defined in cableVariables.default_minCableSingleCoreSize
        :param size: the maximum cable cross sectional area
        :param coretype: whether the core is an active, neutral or earth cable. Default to 'ACTIVE'.
        :return:
        """

        if coretype.upper() == 'ACTIVE':
            if (size is not None) and (size == 'DEFAULT'):
                return self.filter(activeCores__size__lte=cableVar.default_minCableSingleCoreSize)
            if (size is None) or (size < 0):
                pass
                # return self.filter(activeCores__size__lte=0)
            return self.filter(activeCores__size__lte=size)

        if coretype.upper() == 'NEUTRAL':
            if (size is not None) and (size == 'DEFAULT'):
                return self.filter(neutralCores__size__lte=cableVar.default_minCableSingleCoreSize)
            if (size is None) or (size < 0):
                pass
                # return self.filter(neutralCores__size__gte=0)
            return self.filter(neutralCores__size__lte=size)

        # Do not apply a minimum earth conductor size
        if coretype.upper() == 'EARTH':
            if (size is None) or (size < 0) or (size == 'DEFAULT'):
                pass
                # return self.filter(earthCores__size__gte=0)
            return self.filter(earthCores__size__lte=size)

    def find_instpairs(self, number=0, type='DEFAULT'):
        # TODO: Determine a way to determine a query based on two query terms.
        """
        Query based on instrumentation core type (pair or triple) and the number of the pairs/triples.
        :param type: Type of core
        :return:
        """
        if (number is not None) and (number is 'DEFAULT'):
            return self.filter(Q(instPairs__number__=number) & Q(instPairs__name__=cableVar.default_coreName))

    #     if (size is None) or (size < 0):
    #         return self.filter(activeCores__size__gte=0)
    #     return self.filter(activeCores__size__=size)

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
        if (arrangement is not None) and (arrangement.upper() == 'DEFAULT'):
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
        if (armour is not None) and (armour.upper() == 'DEFAULT'):
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
        if (screen is not None) and (screen.upper() == 'DEFAULT'):
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
        if (screen is not None) and (screen.upper() == 'DEFAULT'):
            return self.filter(coreScreen__type__=cableVar.default_coreScreen)
        if (screen is None) or (screen.upper() not in cableVar.list_coreScreen):
            screens = cableVar.list_coreScreen
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(coreScreen__type__=code), screens))
            return self.filter(query)
        return self.filter(coreScreen__type__=screen.upper())

    def find_cableflex(self, flex=None):
        """
        Query based on is flexible cable.
        :param flex:
        :return:
        """
        if (flex is not None) and (flex.upper() == 'DEFAULT'):
            return self.filter(isFlex=cableVar.default_flexCable)
        if (flex is None) or (flex.upper() not in cableVar.list_flexCable):
            types = cableVar.list_flexCable
            query = reduce(lambda q1, q2: q1.__or__(q2),
                           map(lambda code: Q(isFlex=code), types))
            return self.filter(query)
        return self.filter(isFlex=flex.upper())

    def find_cableinstallmethod(self, install_method=None):
        """
        Query to find cables equal to or greater than the passed current carrying capacity.
        :param install_method:
        :return:
        """
        # TODO: Resolve the issue with searching a list.
        if (install_method is not None) and (install_method.upper() == 'DEFAULT'):
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
            return self.filter(neutralCores__number__gte=1)
        if hasneutral is False:
            return self.filter(neutralCores__number__=0)

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
    size = DecimalField(
        precision=1,
        choices=cableVar.list_conductorSize,
        default=cableVar.default_minCableSize
    )

    sizeUnit = StringField(
        choices=cableVar.list_sizeUnit,
        default=cableVar.default_sizeUnit
    )
    number = IntField(
        min_value=0
    )
    name = StringField(
        default='CORE'
    )

    def clean(self):
        """
        Clean up the data provided.
        """
        if self.size is '-':
            self.size = 0
        if self.number is '-':
            self.number = 0
        if self.number == 0:
            self.name = '-'
        self.name = self.name.upper()


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
    # TODO: Modify cables impedance to correct for cableArrange to impendance
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


class Cable(Document):
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
    # TODO: Add method to allow access to parameters.

    meta = {'collection': 'Cable',
            'queryset_class': QueryCable,
            'ordering': [
                # '-conductorMaterial',
                # 'coreArrangement',
                'activeCores__size',
                # 'neutralCores_size',
                # 'earthCores__size',
                # 'manufacturer__name'
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
    # TODO: Should voltRating be an embedded document that allows the phase-earth and phase-phase voltages of the cables to be defined? This would have merit.
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
    #         'earthCores__size__',
    #     )

    def calc_cableDescrtipion(self):
        """
        Method to determine the cable's description from attributes.
        :return: 
        """
        #   TODO: Complete the method.
        pass

    def find_ccc(self, install_method):
        """
        Return the cable's CCC for the given instalation method.

        :param install_method:
        :return:
        """
        try:
            for x in self.installMethod:
                if install_method in x.name:
                    return x.current

        except Exception as e:
            print(e)
            return 0

    def find_mvam(self):
        """
        Return the cable's MVAM value.
        :return:
        """
        return self.impedance.MVAM


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
    cable = Cable(description=details["description"])
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
            # print(cable.description)
            # print("Exception occurred \n {}".format(e))
            pass

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
