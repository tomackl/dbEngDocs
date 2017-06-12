20160319 COPIED INTO PyCharm CE
/* Misc. MongoEngine Classes */

class coreDetails(EmbeddedDocument):
    size = DecimalField(precision=1, choices=<MAPS TO conductorSize IN VARIABLES.CONFIG>)
    sizeUnits = StringField(default=<MAPS TO defaultSizeUnit IN VARIABLES.CONFIG, choices=<MAPS TO sizeUnits IN VARIABLES.CONFIG>)
    number = IntField()

class cableInstallDetails(EmbeddedDocument):
    name = StringField(required=True, choices=<MAPS TO installMethod IN VARIABLES.CONFIG>)
    current = IntField(required=True)
    installTemp = IntField(required=True)

class cableInsulationDetails(EmbeddedDocument):
    name = StringField(required=True, choices=<MAPS TO insulationType IN VARIABLES.CONFIG>)
    conductorTemperature = IntField(choices=<based on insulation classes>) //maximum conductor temperature. Assumes degrees C
    maxTemperature = IntField(choices=<based on insulation classes>)

class cableScreen(EmbeddedDocument):
    type =  StringField(choices=<MAPS TO cableScreen IN VARIABLES.CONFIG>)
    faultWithstand = IntField()

class coreScreen(EmbeddedDocument):
    type =  StringField(choices=<MAPS TO coreScreen IN VARIABLES.CONFIG>)

class cableImpedance(EmbeddedDocument):
    MVAM = DecimalField(precision=4)
    rOhmsPerKM = DecimalField(precision=4) // resistance (ohms/km)
    xOhmsPerKM = DecimalField(precision=4) // reactance (ohms/km)
    zOhmsPerKM = DecimalField(precision=4) // impedance (ohms/km)

class manufacturerDetails(EmbeddedDocument):
    name = StringField()
    partNumber = StringField()

class i2t(EmbeddedDocument):
    kFactor = IntField(required=True)
    // this will probably have to calculated from a look up table and will be unique to each run
    time = ListField(min_value=0.0001, max_value=5, precision=4)
    // this will be a list of time values ranging from 0.0001 to 5 secs. It can zipped with i2t.current shown below.
    current = ListField(min_value=0)
    // this will be a list of current values that be zipped with i2t.time shown above.

class revisionDetail(EmbeddedDocument):
    import datetime
    number = StringField(required=True),
    date = DateTimeField(default=datetime.datetime.now()) /* date of the most recent change */
