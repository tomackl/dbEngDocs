cableArmour = StringField(
        choices=cableVar.list_cableArmour,
        default=cableVar.default_cableArmour
        )
    # TODO: Modify cables impedance to correct for cableArrange to impedance
    cableArrangement = StringField(
        choices=cableVar.list_cableArrangement,
        default=cableVar.default_cableArrangement
    )
    cableMaxParallelRuns = IntField(
        default=cableVar.default_cablesMaxParallel
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