# coding: utf-8
#
from mongoengine import *
import datetime
import config.cableVariables as cableVar
import Cables
import ElectricalFunctions as EF
from functools import reduce

"""
What is a cable run?
0. It performs a specific function. There may be more than one cable run between a given load and supply but each run
  has a discrete purpose, e.g. power, control, instrumentation.
1. Made up of 1 or more cables.
2. Has the lumped characteristics of the cables that it contains.
3. Has a single identifier/tag for the entire run.
4. Has a point-of-supply and a load
5. When exported (e.g. cable schedule) the individual cable details are also exported.
6.
"""
# TODO: Should defaults for cables installed in cable run be included as part of the cable run itself? This would allow
# TODO cont.: defaults for individual runs to be indepentantly set.


class ExceptionCableRun(Exception):
    """
    Base exception for CableRun.py specific exceptions.
    """
    pass


class ExceptionVoltDrop(ExceptionCableRun):
    pass

# ----------- QUERY SETS


class QueryCableRunDetails(QuerySet):
    """
    Class to allow querying of specific cable run details.
    """
    # def find_cable_run_csa(self):
    #     """Query to sum the CSA of a cable run's active cores."""
    #     return self.filter(cables__S__activeCores__size__sum)

    def find_cable_run_type(self, runtype):
        """Query to find cable run type."""
        return self.filter(type=runtype.upper())

    def find_cable_run_current_active_gte(self, amps):
        """Query to find cable runs with active current carrying capacity greater than or equal to some amount."""
        return self.filter(active__current__gte=amps)

    def find_cable_run_current_active_lte(self, amps):
        """Query to find cable runs with active current carrying capacity less than or equal to some amount."""
        return self.filter(active__current__lte=amps)

    def find_cable_run_current_neutral_gte(self, amps):
        """Query to find cable runs with neutral current carrying capacity greater than or equal to some amount."""
        return self.filter(neutral__current__gte=amps)

    def find_cable_run_current_neutral_lte(self, amps):
        """Query to find cable runs with neutral current carrying capacity less than or equal to some amount."""
        return self.filter(neutral__current__lte=amps)

    def find_cable_run_current_earth_gte(self, amps):
        """Query to find cable runs with earth current carrying capacity greater than or equal to some amount."""
        return self.filter(earth__current__gte=amps)

    def find_cable_run_current_earth_lte(self, amps):
        """Query to find cable runs with earth current carrying capacity less than or equal to some amount."""
        return self.filter(earth__current__lte=amps)

    def find_cable_run_voltage(self, voltage):
        """Query to find cable runs with a given voltage"""
        return self.filter(circuit__voltage=voltage)

    def find_cable_run_supply(self, supply):
        """Query to find cable runs connected to a given point-of-supply."""
        return self.filter(supply=supply.upper())

    def find_cable_run_load(self, load):
        """Query to find cable runs connected to a given load."""
        return self.filter(load=load.upper())

    def find_cable_run_contract_supply(self, supplycontract):
        """Query to find cable runs associated with a given supply contract."""
        return self.filter(contract__supply=supplycontract.upper())

    def find_cable_run_contract_install(self, installcontract):
        """Query to find cable runs associated with a given installation contract."""
        return self.filter(contract__install=installcontract.upper())

    def find_cable_run_contract_connect(self, connectcontract):
        """Query to find cable runs associated with a given connection contract."""
        return self.filter(contract__connect=connectcontract.upper())

    # def find_empty_cable_run(self):
    #     """Query to find cable runs without any cables."""
    #     # i = len(self.cables)
    #     return self.filter(cables==0)


class CableRunDefault(EmbeddedDocument):
    """
    Mongo Engine class allowing the storage of default values associated with a cable run. 
    The class allows a range of values to be defined for each cable run where a single specific requirement is not 
    defined or strictly required.  
    """
    cableArmour = StringField(
        choices=cableVar.list_cableArmour,
        default=cableVar.default_cableArmour
        )
    # TODO: Modify cables impedance to correct for cableArrange to impedance
    cableArrangement = StringField(
        choices=cableVar.list_cableArrangement,
        default=cableVar.default_cableArrangement
    )
    cableMultiCoreMin = DecimalField(
            precision=1,
            choices=cableVar.list_conductorSize,
            default=cableVar.default_minCableSize
    )
    cableMultiCoreMax = DecimalField(
            precision=1,
            choices=cableVar.list_conductorSize,
            default=cableVar.default_minCableSingleCoreSize
    )
    cableSingleCoreMin = DecimalField(
            precision=1,
            choices=cableVar.list_conductorSize,
            default=cableVar.default_minCableSingleCoreSize
    )
    cableSingleCoreMax = DecimalField(
            precision=1,
            choices=cableVar.list_conductorSize,
            default=cableVar.list_conductorSize[-1]
    )
    cableFlexible = StringField(
        choices=cableVar.list_flexCable,
        default=cableVar.default_flexCable
    )
    cableInsulationCode = ListField(
        StringField(
            choices=cableVar.list_insulationCode,
            default=cableVar.default_insulationCode
        )
    )
    cableScreen = StringField(
        choices=cableVar.list_cableScreen,
        default=cableVar.default_cableScreen
    )
    cableShape = ListField(
        StringField(
            choices=cableVar.list_cableShape,
            default=cableVar.default_cableShape
        )
    )
    cableSheath = StringField(
        choices=cableVar.list_sheathType,
        default=cableVar.default_sheathType
    )
    cableType = StringField(
        choices=cableVar.list_cableType
    )
    cableVoltRating = ListField(
        StringField(
            choices=cableVar.list_voltRating,
            default=cableVar.default_voltRating
        )
    )
    # TODO: Delete below sel.type already exists
    # circuitType = ListField(
    #     StringField(
    #         choices=cableVar.list_circuitType,
    #         default=cableVar.default_circuitType
    #     )
    # )
    conductorMaterial = StringField(
        choices=cableVar.list_conductorMaterial,
        default=cableVar.default_conductorMaterial
    )
    # The below may be replaced by the single and multi-core defaults described above.
    coreArrangement = ListField(
        StringField(
            choices=cableVar.list_coreArrangement,
            default=cableVar.default_coreArrangement
        )
    )
    # coreArrangementAllSingleCore defines whether single core cables can be used. It should be referenced where there
    # is a need to check for whether single core cables are allowed. This won't check coreArrangement (above) for the
    # presence of single core cables since this will be defined by the user.
    coreArrangementAllowSingleCore = BooleanField(
        default=True,
        required=True
    )
    coreScreen = StringField(
        choices=cableVar.list_coreScreen,
        default=cableVar.default_coreScreen
    )
    manufacturerName = StringField()
    manufacturerPartNumber = StringField()

    def clean(self):
        """
        Validation of the initial values.
        :return: 
        """
        # TODO: Add cableSheath
        if not self.cableMultiCoreMin:
            self.cableMultiCoreMin = cableVar.default_minCableSize
        if not self.cableMultiCoreMax:
            self.cableMultiCoreMax = cableVar.list_conductorSize[-1]
        if not self.cableSingleCoreMin:
            self.cableSingleCoreMin = cableVar.default_minCableSingleCoreSize
        if not self.cableSingleCoreMax:
            self.cableSingleCoreMax = cableVar.list_conductorSize[-1]
        if not self.cableArmour:
            self.cableArmour = cableVar.default_cableArmour
        if not self.cableArrangement:
            self.cableArrangement = cableVar.default_cableArrangement
        if not self.cableFlexible:
            self.cableFlexible = cableVar.default_flexCable
        if len(self.cableInsulationCode) == 0:
            self.cableInsulationCode.append(cableVar.default_insulationCode)
        if not self.cableScreen:
            self.cableScreen = cableVar.default_cableScreen
        if len(self.cableShape) == 0:
            self.cableShape.append(cableVar.default_cableShape)
        # TODO: This may need to be reassessed on some level.
        # if self.circuitType.upper() is ('MULTI' or 'SINGLE'):
        #     self.cableType = 'POWER'
        if len(self.cableVoltRating) == 0:
            self.cableVoltRating.append(cableVar.default_voltRating)
        # if len(self.circuitType) == 0:
        #     self.circuitType.append(cableVar.default_circuitType)
        if len(self.coreArrangement) == 0:
            self.coreArrangement.append(cableVar.default_coreArrangement)
        if not self.coreScreen:
            self.coreScreen = cableVar.default_coreScreen
        # if self.coreArrangementAllowSingleCore == ('TRUE' or 'YES'):
        #     self.coreArrangementAllowSingleCore = True
        # if self.coreArrangementAllowSingleCore == ('FALSE' or 'NO' or 'NIL'):
        #     self.coreArrangementAllowSingleCore = False
        if self.manufacturerName:
            self.manufacturerName = self.manufacturerName.upper()
        if self.manufacturerPartNumber:
            self.manufacturerPartNumber = self.manufacturerPartNumber.upper()

        # print('default cleaned')


class ConductorDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable run conductor.
    It relies on cable variables configuration file being present to check the preferred details.

    size: cross sectional area
    sizeUnit: cross sectional area unit of measure
    number: number of cores
    """
    size = DecimalField(
        precision=1,
        default=0
    )
    sizeUnit = StringField(
        choices=cableVar.list_sizeUnit,
        default=cableVar.default_SizeUnit
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
    date = DateTimeField(
        default=datetime.datetime.now()
    )

    def clean(self):
        self.number = self.number.upper()


class CableRunConductor(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of the cable run's lumped conductors.

    active: the cable run's lumped active conductor
    neutral: the cable run's lumped neutral conductor
    earth: the cable run's lumped earth conductor
    """

    active = EmbeddedDocumentField(
        ConductorDetails,
        required=True
    )
    neutral = EmbeddedDocumentField(
        ConductorDetails,
        required=True
    )
    earth = EmbeddedDocumentField(
        ConductorDetails,
        required=True
    )


class Impedance(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable run's impedance
    details.
    It relies on cable variables configuration file being present to check the
    preferred details.

    MVAM: Milli-volts per amp-metre
    rOhms: resistance (ohms)
    xOhms: reactance (ohms)
    zOhms: impedance (ohms)
    """
    MVAM = DecimalField(
        precision=4,
        min_value=0,
        default=0
    )
    rOhms = DecimalField(
        precision=4,
        min_value=0,
        default=0
    )
    xOhms = DecimalField(
        precision=4,
        min_value=0,
        default=0
    )
    zOhms = DecimalField(
        precision=4,
        min_value=0,
        default=0
    )


class Contracts(EmbeddedDocument):
    """
    A simple class to store details associated with with installation contracts.
    """
    #  TODO: the contract fields should be made a reference field when the contracts collection is made.
    supply = StringField()
    install = StringField()
    connect = StringField()

    def clean(self):
        if self.supply is None:
            self.supply = ''
        else:
            self.supply = self.supply.upper()
        if self.install is None:
            self.install = ''
        else:
            self.install = self.install.upper()
        if self.connect is None:
            self.connect = ''
        else:
            self.connect = self.connect.upper()


class ElecDetails(EmbeddedDocument):
    """
    Mongo Engine data checking class.
    This class defines and checks the voltage details of a cable run.
    voltage: voltage of the circuit. This is assumed to reflect the number of phases of the circuit. Where a
        multi-phase circuit exists the phase to earth voltage is expected to be calculated by the application rather
        than be stored within the DB itself. self.phases is intended to be checked by the calling app.
    phases: the number of phases
    waveform: is the circuit AC or DC?
    CCC: the circuit's lumped current carrying capacity
    """
    voltage = IntField(
        # The cable run's primary voltage. Used to select cables.
        # TODO: Consider possible impact on trailing cables and similar cables.
        required=True,
        choices=cableVar.list_circuitVoltage
    )
    phases = IntField(
        # Number of phases required by the cable run.
        min_value=1,
        max_value=3,
        required=True
    )
    waveform = StringField(
        # AC or DC circuit
        required=True,
        choices=cableVar.list_circuitCurrent
    )
    CCC = IntField(
        # Current carrying capacity of the cable run. This is the sum of all active conductors in the run.
        min_value=0,
        required=True,
        default=0
    )
    loadCurrent = DecimalField(
        # Load's full load current (I_flc)
        min_value=0,
        precision=1
    )
    derating = DecimalField(
        # Cable run derating factor
        min_value=0.1,
        max_value=1.0,
        precision=2,
        rounding='ROUND_HALF_DOWN',
        default=1.0
    )
    installMethod = StringField(
        # The run's installation method
        choices=cableVar.list_installMethod,
        default=cableVar.default_installMethod
    )
    requiresNeutral = BooleanField(
        # Does the cable run require a neutral conductor
        required=True,
        default=True
    )
    maxVd = DecimalField(
        # The maximum allowable volt drop across the cable run in percent.
        min_value=0,
        max_value=0.5,
        precision=2,
        default=0.03,  # Default to 3%
        required=True
    )
    Vd = DecimalField(
        # The calculated volt drop across the cable run.
        min_value=0,
        precision=2
    )

    def clean(self):
        self.waveform = self.waveform.upper()
        self.installMethod = self.installMethod.upper()


class CableRun(Document):
    # TODO: Add a protection device to run or make reference to PD in supply
    """
    Mongo Engine data checking class.
    This class defines and checks the details of a cable run.
    It relies on the cable variables configuration file being present to  the
    preferred details being present.

    _tag_: Cable run tag. This is *not* being used as a key and nor should it.
    _length_: The cable run length.
    _cables_: a list of the cables that make up the run.
    _activeConductor_: details of the run's active conductor. This is a lumped
        value based on the cables contained within the cables list.
    _neutralConductor_: details of the run's neutral conductor. This is a lumped value based on the cables contained
        within the cables list.
    _earthConductor_: details of the run's earth conductor. This is a lumped value based on the cables contained within
        the cables list.
    _description_: an abbreviated description of the cable run based on the cables that make up the run.
    _supply_: tag of the cable run's point-of-supply
    _load_: tag of the cable run's load
    _notes_: a field to allow notes to be recorded against the cable run
    _type_: the type of circuit the cable run is. As per list_cableType.
    _voltage_: the voltage of the cable run's circuit.
    """
    meta = {'collection': 'CableRun',
            'queryset_class': QueryCableRunDetails
            }

    circuit = EmbeddedDocumentField(
        ElecDetails
    )
    impedance = EmbeddedDocumentField(
        Impedance,
        required=True
    )
    conductor = EmbeddedDocumentField(
        CableRunConductor,
        required=True
    )
    tag = StringField(
        required=True,
        unique=True
    )
    length = FloatField(
        min_value=0,
        precision=1,
        required=True
    )
    cables = ListField(
        ReferenceField(Cables.Cable)
        # required=True
    )
    description = StringField()
    # TODO: supply and load should be changed to reference fields when the contracts collection is set up.
    supply = StringField(
        required=True
    )
    load = StringField(
        required=True
    )
    # TODO: notes requires some consideration about what is actually required of it.
    notes = StringField()
    # TODO: type requires the choices to be defined at some point.
    type = StringField(
        choices=cableVar.list_circuitType,
        default=cableVar.default_circuitType,
        required=True
    )
    contract = EmbeddedDocumentField(
        Contracts
    )
    rev = EmbeddedDocumentField(
        RevisionDetail,
        required=True
    )
    default = EmbeddedDocumentField(
        CableRunDefault,
        required=True
    )

    def clean(self):
        """
        Clean up values before importing.
        """
        if self.description is None:
            self.description = ''
        else:
            self.description = self.description.upper()
        self.supply = self.supply.upper()
        self.load = self.load.upper()
        if self.type.upper() == 'DEFAULT':
            self.type = cableVar.default_cableType
        else:
            self.type = self.type.upper()

        # print('cable run cleaned')

    def calc_csa(self):
        """
        Calculate the cable run conductor's total cross sectional area for each conductor. Calculate all at the same time to avoid errors.
        This function will calculate the total cross sectional area of the conductor.
        :return:
        """
        # TODO: Determine how to get this to run (and work) after creating a new run.
        self.reload()
        csa_active = 0
        csa_neutral = 0
        csa_earth = 0

        for each in self.cables:
            cable = Cables.Cable.objects.find_specificcable(each.id).no_dereference().first()
            try:
                csa_active += cable.activeCores.size
                csa_neutral += cable.neutralCores.size
                csa_earth += cable.earthCores.size
            except Exception as e:
                print(e)

        self.update(set__conductor__active__size__=csa_active)
        self.update(set__conductor__neutral__size__=csa_neutral)
        self.update(set__conductor__earth__size__=csa_earth)
        self.reload()

    def calc_impedence(self):
        """
        Calculate the cable run's lumped impedances.
        :return:
        """
        self.reload()
        mvam = []
        r = []
        x = []
        z = []
        length = self.length
        for each in self.cables:
            cable = Cables.Cable.objects.find_specificcable(each.id).first()

            try:
                mvam.append(float(cable.impedance.MVAM))
                r.append(float(cable.impedance.rOhmsPerKM))
                x.append(float(cable.impedance.xOhmsPerKM))
                z.append(float(cable.impedance.zOhmsPerKM))

            except Exception as e:
                print(e)

        self.update(impedance__MVAM=(EF.calculateparallelohms(mvam)))
        self.update(impedance__rOhms=(EF.calculateparallelohms(r) * length / 1000))
        self.update(impedance__xOhms=(EF.calculateparallelohms(x) * length / 1000))
        self.update(impedance__zOhms=(EF.calculateparallelohms(z) * length / 1000))
        self.reload()

    def calc_CCC(self):
        """
        Calculate the cable run's various lumped current carrying capacity.
        :return:
        """
        # TODO: Determine how to get this to run (and work) after creating a new run.
        self.reload()
        ccc = 0

        for each in self.cables:
            cable = Cables.Cable.objects.find_specificcable(each.id).no_dereference().first()
            ccc += self.find_cable_CCC(cable)

        ccc = ccc * self.circuit.derating
        self.update(circuit__CCC=ccc)
        self.reload()

    def find_cable_CCC(self, cable):
        """
        Return the cable's CCC based on the cable run's attributes.
        :param cable:
        :return: cable CCC
        """
        try:
            for x in cable.installMethod:
                if self.circuit.installMethod in x.name:
                    return x.current

        except Exception as e:
            print(e)

    def calc_description(self):
        """
        Calculate the cable run's description from the cables contained within the run.
        :return:
        """
        pass

    def calc_runVd(self):
        """
        Calculate the cable run's voltage drop.
        :return:
        """
        # Reload the cable run to ensure that the actual cable run attributes are present to be used.
        self.reload()
        # Check whether cable run has a MVAM impedence. If it does, use this value.
        if float(self.impedance.MVAM) > 0.0:
            Vd = EF.mvamvoltagedrop(self.length, float(self.circuit.loadCurrent), float(self.impedance.MVAM))
        # If MVAM not present use ohmic values.
        else:
            Vd = EF.ohmvoltagedrop(self.length, self.circuit.loadCurrent, float(self.impedance.rOhms), float(self.impedance.xOhms), float(self.impedance.zOhms))
        self.update(circuit__Vd=Vd)
        self.reload()

    def add_cable(self, cable):
        """
        Add a cable to the cable run.
        :return:
        """
        self.reload()
        for each in cable:
            self.update(push__cables=each)
        self.save()
        self.reload()

    def clear_cable(self):
        """
        Clear cables from the cable run.
        :return:
        """
        self.update(cables=[])
        self.reload()

    def show_cables(self):
        """
        Show the cables contained within the cable run.
        :return:
        # """
        self.reload()
        x = []
        for each in self.cables:
            cable = Cables.Cable.objects.find_specificcable(each.id).first()
            x.append(cable)
        return x

    def query_cable(self, coretype='ACTIVE'):
        """
        This query is meant to be an improvement on the one immediately below. It will use the <default> values 
        contained within the <cableRun> to generate the query. The intent is to string together a query based on these 
          values using the Q functions and map-reduce methods.
        :param coretype: 
        :return: 
        """
        # TODO: Something is required to allow the auto generation of min and max cable sizes based on core type.

        # or_list = []
        and_list = []
        min_cable = []
        max_cable = []
        arrangement = []


        # _or_ the attributes below together

        min_cable.append(self.default.cableMultiCoreMin)
        max_cable.append(self.default.cableMultiCoreMax)

        for x in self.default.coreArrangement:
            arrangement.append(x)

        if self.default.coreArrangementAllowSingleCore is True:
            min_cable.append(self.default.cableSingleCoreMin)
            max_cable.append(self.default.cableSingleCoreMax)
            arrangement.append('1C')

        print(arrangement)

        if coretype.upper() == 'ACTIVE':
            query = map(lambda arrangement, min_cable, max_cable:
                        Q(coreArrangement=arrangement,
                          activeCores__size__gte=min_cable,
                          activeCores__size__lte=max_cable),
                        arrangement, min_cable, max_cable
                        )
            query = reduce(lambda q1, q2: q1.__or__(q2), query)
            and_list.append(query)

        if coretype.upper() == 'NEUTRAL':
            query = map(lambda arrangement, min_cable, max_cable:
                               Q(coreArrangement=arrangement,
                                 neutralCores__size__gte=min_cable,
                                 neutralCores__size__lte=max_cable),
                               arrangement, min_cable, max_cable
                               )
            query = reduce(lambda q1, q2: q1.__or__(q2), query)
            and_list.append(query)

        if coretype.upper() == 'EARTH':
            query = map(lambda arrangement, min_cable, max_cable:
                               Q(coreArrangement=arrangement,
                                 earthCores__size__gte=min_cable,
                                 earthCores__size__lte=max_cable),
                               arrangement, min_cable, max_cable

                           )
            query = reduce(lambda q1, q2: q1.__or__(q2), query)
            and_list.append(query)

        and_list.append(Q(installMethod__name=self.circuit.installMethod))
        and_list.append(Q(circuitType=self.type))
        # TODO: Below is a hack job to sort the cable type information → a tidier solution is required.
        if self.type.upper() is ('MULTI' or 'SINGLE'):
            cableType = 'POWER'
            and_list.append(Q(cableType=cableType))
        # print(and_list)
        # >>>>>>>>>>>>>>> cableType → add

        # TODO: Modify cables impedance to correct for cableArrange to impendence
        # # if self.default.cableArrangement:
        # #     and_list.append(Q(cableArrangement=self.default.cableArrangement))

        if self.default.conductorMaterial:
            and_list.append(Q(conductorMaterial=self.default.conductorMaterial))

        if self.default.cableInsulationCode:
            query = reduce(lambda q1, q2: q1 | q2,
                           map(lambda code:
                               Q(insulation__code=code), self.default.cableInsulationCode)
                           )
            and_list.append(query)

        if self.default.cableSheath:
            and_list.append(Q(sheath=self.default.cableSheath))

        if self.default.cableVoltRating:
            query = reduce(lambda q1, q2: q1 | q2,
                           map(lambda code:
                               Q(voltRating=code), self.default.cableVoltRating)
                           )
            and_list.append(query)

        if self.default.cableShape:
            query = reduce(lambda q1, q2: q1 | q2,
                           map(lambda code:
                               Q(cableShape=code), self.default.cableShape)
                           )
            and_list.append(query)

        if self.default.cableArmour:
            and_list.append(Q(armoured=self.default.cableArmour))

        if self.default.cableFlexible:
            and_list.append(Q(isFlex=self.default.cableFlexible))

        # if self.default.manufacturerName:
        #     and_list.append(Q(manufacturer__name__=self.default.manufacturerName))
        #
        # if self.default.manufacturerPartNumber:
        #     and_list.append(Q(manufacturer__partNumber__=self.default.manufacturerPartNumber))
        x =  Cables.Cable.objects(reduce(lambda q1, q2: q1 & q2, and_list)).sort_corearrangement()
        for each in x:
            print("-- {}".format(each.description))
        return x

    # def query_cable1(self, minconductorsize='DEFAULT', maxconductorsize='DEFAULT', conductorsizeunit='DEFAULT', coretype='ACTIVE', cabletype='DEFAULT', corearrangement=None, activeconductorsize='DEFAULT', cablescreen='DEFAULT', corescreen='DEFAULT', insulationcode='DEFAULT', insulationname='DEFAULT', sheath='DEFAULT', voltrating='DEFAULT', isflex='DEFAULT', armoured='DEFAULT', conductormaterial='DEFAULT', cableshape='DEFAULT'):
    #     # TODO: Update query to search for manufacturer
    #     # TODO: Resolve the issue with cable arrangement
    #
    #     """
    #     Size a cable to allow it to be added to the cable run.
    #     :param minconductorsize:
    #     :param maxconductorsize:
    #     :param conductorsizeunit:
    #     :param coretype:
    #     :param cabletype:
    #     :param corearrangement: number of cores and type. E.g. 3C+E, 6Pr, etc
    #     :param cablearrangement:
    #     :param activeconductorsize: minimum conductor size to start query
    #     :param cablescreen: does the cable require a screen?
    #     :param corescreen: do the cable cores require screens?
    #     :param insulationcode: the cable's insulation code. E.g. X-90, V-75, etc.
    #     :param insulationname:
    #     :param sheath:
    #     :param voltrating:
    #     :param isflex:
    #     :param armoured:
    #     :param conductormaterial:
    #     :param cableshape:
    #     :param manufacturer:
    #     :return: A cable that meets the requirements of the sizing criteria.
    #     """
    #     min_conductor_size = minconductorsize
    #     max_conductor_size = maxconductorsize
    #     core_type = coretype
    #     conductor_size_unit = conductorsizeunit
    #     requires_neutral = self.circuit.requiresNeutral
    #     load_current = self.circuit.loadCurrent
    #     cable_type = cabletype
    #     circuit_type = "DEFAULT"
    #     if (self.circuit.phases > 1) and (self.type.upper() == 'POWER'):
    #         circuit_type = "MULTI"
    #     if (self.circuit.phases == 1) and (self.type.upper() == 'POWER'):
    #         circuit_type = "SINGLE"
    #
    #     core_arrangement = corearrangement
    #     # cable_arrangement = cablearrangement
    #     active_conductor_size = activeconductorsize
    #     install_method = self.circuit.installMethod
    #     cable_screen = cablescreen
    #     core_screen = corescreen
    #     insulation_code = insulationcode
    #     insulation_name = insulationname
    #     sheath = sheath
    #     volt_rating = voltrating
    #     is_flex = isflex
    #     armoured = armoured
    #     conductor_material = conductormaterial
    #     cable_shape = cableshape
    #     # manufacturer = manufacturer
    #
    #     x = Cables.Cable.objects\
    #         .find_cablecurrent_gte(install_method, load_current)\
    #         .find_hasneutral(requires_neutral)\
    #         .find_conductorsize(min_conductor_size, core_type)\
    #         .find_maxconductorsize(max_conductor_size, core_type)\
    #         .find_conductorsizeunit(conductor_size_unit)\
    #         .find_cabletype(cable_type)\
    #         .find_conductorsize(active_conductor_size)\
    #         .find_cablescreen(cable_screen)\
    #         .find_corescreen(core_screen)\
    #         .find_insulationcode(insulation_code)\
    #         .find_insulationtype(insulation_name)\
    #         .find_cablesheath(sheath)\
    #         .find_voltrating(volt_rating)\
    #         .find_cableflex(is_flex).find_cableshape(cable_shape)\
    #         .find_cablearmour(armoured)\
    #         .find_conductormaterial(conductor_material)\
    #         .find_corearrangement(core_arrangement) \
    #         .find_circuittype(circuit_type) \
    #         .sort_corearrangement()\
    #         .sort_activesize()
    #
    #     # .find_manufacturername(manufacturer)
    #     # .find_cablearrangement(cable_arrangement)
    #     # if len(x) == 0:
    #     #     print("HAHA")
    #     # for each in x:
    #     #     print(each.description)
    #     return x

    def check_CCC(self, cable=None):
        """
        Check whether the cable run current carrying capacity is greater than the load current. If a cable object is not
        passed then assume that the cable run's CCC is being checked.
        Derating is applied to the cable run. Return True or False as appropriate.
        :param cable: if
        :return:
        """
        try:
            if (cable.find_ccc(self.circuit.installMethod) * self.circuit.derating) > self.circuit.loadCurrent:
                return True
            else:
                return False
        except TypeError as e:
            if cable is None:
                if (self.circuit.CCC * self.circuit.derating) > self.circuit.loadCurrent:
                    return True
                else:
                    return False
            else:
                print(e)

    def check_cable_vd(self, cable):
        """
        Check whether the cable run volt drop is less then the maximum volt drop. Return True or False as appropriate.
        :param cable:
        :return:
        """
        volt_drop = EF.mvamvoltagedrop(
            float(self.length),
            float(self.circuit.loadCurrent),
            float(cable.find_mvam())
        )
        if volt_drop < (float(self.circuit.maxVd) * float(self.circuit.voltage)):
            return True
        else:
            return False

    def size_cablerun(self, **kwargs):
        """
        A method to allow the sizing of cable run cables.
        :return:
        """

        cable_query = self.query_cable(**kwargs)
        # i = len(cable_query)
        if self.find_cable(cable_query) is False:
            print(self.description)

    def find_cable(self, cable_query):
        """
        Find a cable that meets the cable run's requirements. If found return True, else return False.
        :return:
        """
        for cable in cable_query:
            print(":: {}" .format(cable.description))
            x = []
            if (self.check_CCC(cable) and self.check_cable_vd(cable)) is True:
                self.clear_cable()
                x.append(cable)
                self.add_cable(x)
                self.bulk_calc()
                return True
        return False

    def bulk_calc(self):
        """
        Calculate all the run's calculated attributes.
        :return:
        """
        self.calc_csa()
        self.calc_CCC()
        self.calc_impedence()
        self.calc_runVd()

    def size_single_cables(self):
        """
        Method will allow the sizing of single core cable cable runs.
        :return:
        """
        pass


# <------- IMPORT FUNCTIONS


def new_cable_run(supply=None, load=None, cables=[], loadcurrent=0, length=0, derating=1, voltage=0, voltdrop=0.03, installationmethod=None, phases=0, waveform='AC', runtype=None, tag=None, revNumber=None, requiresneutral=True, contractsupply=None, contractinstall=None, contractconnect=None, notes=None, description=None, mvam=0, r_ohms=0, x_ohms=0, z_ohms=0, **kwargs):
    """
    # Create a new cable run.
    :param supply:
    :param load:
    :param cables:
    :param loadcurrent:
    :param length:
    :param derating:
    :param voltage:
    :param voltdrop:
    :param installationmethod:
    :param phases:
    :param waveform:
    :param runtype:
    :param tag:
    :param revNumber:
    :param requiresneutral:
    :param contractsupply:
    :param contractinstall:
    :param contractconnect:
    :param notes:
    :param description:
    :param mvam: Actual impedance details should be calculated after cableRun instantiated.
    :param r_ohms: Actual impedance details should be calculated after cableRun instantiated.
    :param x_ohms: Actual impedance details should be calculated after cableRun instantiated.
    :param z_ohms: Actual impedance details should be calculated after cableRun instantiated.
    :return:
    """
    # TODO: Add description of additional keywords that can be passed to the function to allow that impact of cable selection e.g. conductor material, insulation etc. If these exist these will be passed to the cable selection function to allow querying of the database.
    # TODO: consolidate with add_cablerun_dict to reduce code redundancy
    cableRun = CableRun()
    cableRun.supply = supply
    cableRun.load = load
    if len(cables) != 0:
        for each in cables:
            cableRun.cables.append(each)
    cableRun.length = length
    cableRun.circuit = ElecDetails(
        loadCurrent=loadcurrent,
        voltage=voltage,
        phases=phases,
        waveform=waveform,
        derating=derating,
        installMethod=installationmethod,
        requiresNeutral=requiresneutral,
        maxVd=voltdrop
    )
    cableRun.impedance = Impedance(
        MVAM=mvam,
        rOhms=r_ohms,
        xOhms=x_ohms,
        zOhms=z_ohms
    )
    cableRun.conductor = CableRunConductor()
    cableRun.conductor.active = ConductorDetails()
    cableRun.conductor.neutral = ConductorDetails()
    cableRun.conductor.earth = ConductorDetails()
    # cableRun.circuit = ElecDetails()
    cableRun.type = runtype
    cableRun.tag = tag
    cableRun.rev = RevisionDetail(
        number=revNumber
    )
    cableRun.contract = Contracts(
        supply=contractsupply,
        install=contractinstall,
        connect=contractconnect
    )
    cableRun.notes = notes
    cableRun.description = description
    cableRun.save()


def import_cablerun_data(db, filepath):
    """
    Import cable run data and add to the database.
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
                add_cablerun_dict(each)
            else:
                print("NOT A DICT!!")

    except Exception as e:
        print(e)
    finally:
        generator.close()


def add_cablerun_dict(details):
    # TODO: Determine a CSV header system to allow importing of data.
    # TODO: Allow update of existing cable runs.
    """
    This function is designed for the importation of cables run details from a CSV file.

    The function will do some error checking before the MongoEngine's checks. These checks are simple and are intended
    to be basic data entry formatting type checks.
    :param details:  cable run details contained within a dict.
    :return:
    """

    cableRun = CableRun(description=details["description"])
    cableRun.circuit = ElecDetails()

    if 'circuit.CCC' in details:
        cableRun.circuit.CCC = details['circuit.CCC']

    if 'circuit.vd' in details:
        cableRun.circuit.vd = details['circuit.vd']

    if "circuit.voltage" in details:
        cableRun.circuit.voltage = int(details["circuit.voltage"])

    if "circuit.phases" in details:
        cableRun.circuit.phases = details["circuit.phases"]

    if "circuit.waveform" in details:
        cableRun.circuit.waveform = details["circuit.waveform"]

    if "circuit.loadCurrent" in details:
        cableRun.circuit.loadCurrent = details["circuit.loadCurrent"]

    if "circuit.derating" in details:
        cableRun.circuit.derating = details["circuit.derating"]

    if "circuit.installMethod" in details:
        cableRun.circuit.installMethod = details["circuit.installMethod"]

    if "circuit.requiresNeutral" in details:

        if details["circuit.requiresNeutral"].upper() is 'TRUE':
            cableRun.circuit.requiresNeutral = True

        if details["circuit.requiresNeutral"].upper() is 'FALSE':
            cableRun.circuit.requiresNeutral = False

    if "circuit.maxVd" in details:
        cableRun.circuit.maxVd = details["circuit.maxVd"]

    cableRun.tag = details["tag"]
    cableRun.length = float(details["length"])

    try:
        for each in details["cables"]:
            cableRun.cables.append(each)
    except Exception as e:
        print(e)

    if "type" in details:
        cableRun.type = details["type"]

    cableRun.conductor = CableRunConductor()
    cableRun.conductor.active = ConductorDetails()
    cableRun.conductor.neutral = ConductorDetails()
    cableRun.conductor.earth = ConductorDetails()
    cableRun.supply = details["supply"]
    cableRun.load = details["load"]

    if "notes" in details:
        cableRun.notes = details["notes"]

    cableRun.contract = Contracts(
        supply=details["contract.supply"],
        install=details["contract.install"],
        connect=details["contract.connect"]
    )

    cableRun.rev = RevisionDetail(
        number=details["rev.number"],
        date=datetime.datetime.now()
        )

    cableRun.impedance = Impedance()

    if 'circuit.MVAM' in details:
        cableRun.MVAM = details['details.MVAM']

    if 'circuit.rOhms' in details:
        cableRun.rOhms = details['detailsrOhms']

    if 'circuit.xOhms' in details:
        cableRun.xOhms = details['details.xOhms']

    if 'circuit.zOhms' in details:
        cableRun.zOhms = details['details.zOhms']
    cableRun.default = CableRunDefault()
    if 'default.cableArmour' in details:
        cableRun.default.cableArmour = details['default.cableArmour']
    if 'default.cableArrangement' in details:
        cableRun.default.cableArrangement = details['default.cableArrangement'].upper()
    if 'default.MultiCoreMin' in details:
        cableRun.default.MultiCoreMin = details['default.MultiCoreMin']
    if 'default.MultiCoreMax' in details:
        cableRun.default.MultiCoreMax = details['default.MultiCoreMax']
    if 'default.SingleCoreMax' in details:
        cableRun.default.SingleCoreMax = details['default.SingleCoreMax']
    if 'default.SingleCoreMin' in details:
        cableRun.default.SingleCoreMin = details['default.SingleCoreMin']

    if 'default.cableFlexible' in details:
        if details['default.cableFlexible'].upper() is ('TRUE' or 'YES'):
            cableRun.default.cableFlexible = True

        if details['default.cableFlexible'].upper() is ('FALSE' or 'NO' or 'NIL'):
            cableRun.default.cableFlexible = False

    if 'default.cableInsulationCode' in details:
        x = details['default.cableInsulationCode'].split(',')
        for each in x:
            cableRun.default.cableInsulatonCode.append(each.upper())

    if 'default.cableScreen' in details:
        cableRun.default.cableScreen = details['default.cableScreen'].upper()

    if 'default.cableShape' in details:
        x = details['default.cableShape'].split(',')
        for each in x:
            cableRun.default.cableShape.append(each.upper())
        # cableRun.default.cableShape = details['default.cableShape'].upper()

    if 'default.cableSheath' in details:
        cableRun.default.cableSheath = details['default.cableSheath'].upper()

    if 'default.cableVoltRating' in details:
        x = details['default.cableVoltRating'].split(',')
        for each in x:
            cableRun.default.cableVoltRating.append(each.upper())
        # cableRun.default.cableVoltRating = details['default.cableVoltRating'].upper()

    if 'default.coreArrangement' in details:
        x = details['default.coreArrangement'].split(',')
        for each in x:
            cableRun.default.coreArrangement.append(each.upper())
        # cableRun.default.coreArrangement = details['default.coreArrangement'].upper()

    if 'default.coreArrangementAllowSingleCore' in details:
        if details['default.coreArrangementAllowSingleCore'].upper() is ('TRUE' or 'YES'):
            cableRun.default.coreArrangementAllowSingleCore = True

        if details['default.coreArrangementAllowSingleCore'].upper() is ('FALSE' or 'NO' or 'NIL'):
            cableRun.default.coreArrangementAllowSingleCore = False

    if 'default.manufacturerName' in details:
        cableRun.default.manufacturerName = details['default.manufacturerName'].upper()
    if 'default.manufacturerPartNumber' in details:
        cableRun.default.manufacturerPartNumber = details['default.manufacturerPartNumber'].upper()
    cableRun.save()
