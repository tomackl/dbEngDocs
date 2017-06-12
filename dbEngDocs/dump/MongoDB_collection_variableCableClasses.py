class cableVariable(Document):
    fileDetails =
    "DB": "dbEngDocs",
    "collection": "CableDetails",
    "file": ".config"
  },
list_cableType = ListField(StringField())
list_circuitType = ListField(StringField())
list_conductorMaterial = ListField(StringField())
default_conductorMaterial = StringField(choices=conductorMaterial)
list_installMethod = ListField(StringField())
list_cableArrangement = ListField(StringField())
list_sheathType = ListField(StringField())
list_insulationType = ListField(StringField())
list_voltRating = ListField(StringField())
default_voltRating = StringField(choices = voltRating)
list_circuitVoltage = ListField(IntField())
list_circuitCurrent = ListField(StringField())
list_conductorSize = ListField(DecimalField(precision=1))
default_conductorSize = DecimalField(precision=1)
minCableSingleCoreSize = DecimalField(precision=1, choices=conductorSize)
list_sizeUnit = ListField(StringField())
default_SizeUnit = StringField(choices = sizeUnits)
list_coreArrangements = ListField(StringField())
list_cableArmour = ListField(StringField())
default_cableArmour = StringField(choices = cableArmour)
list_cableScreen = ListField(StringField())
default_cableScreen = StringField(choices=cableScreen)
list_coreScreen = ListField(StringField())
default_coreScreen = StringField(choices=coreScreen)
list_power = DictField()
list_flexCable = ListField(StringField())
default_flexCable = StringField(choices=flexCable)
default_deratingFactor = DecimalField(precision=1)
