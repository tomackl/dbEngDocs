#
# coding: UTF-8
#
from mongoengine import *
import datetime


# Is this actually required? If may be easier to allow this to be managed by the existing .py file.
"""
This module defines the documents that will contain the databases default values. The values stored within 
cableVariables.py will be transferred to the database. 
"""


class CircuitDefault(EmbeddedDocument):
    """
    General defaults that relate to the circuits.
    """
    list_circuitType = ListField(
        StringField,
        required=True
    )
    default_circuitType = StringField(
        choices=list_circuitType,
        required=True
    )
    list_installMethod = ListField(
        StringField,
        required=True
    )
    default_installMethod = StringField(
        choices=list_installMethod,
        required=True
    )
    list_circuitVoltage = ListField(
        IntField,
        required=True
    )
    list_circuitCurrent = ListField(
        DecimalField(
            precision=1
        ),
        required=True
    )
    list_power = MapField(
        IntField,
        required=True
    )


class CableRunDefault(EmbeddedDocument):
    """
    This embedded document contains the variables that are specifically related to cable runs.
    """
    cablesMaxParallel = IntField(
        required=True
    )
    cableAllowParallelMulti = IntField(
        required=True
    )


class CableDefault(EmbeddedDocument):
    """
    This embedded document contains the variables that are specifically related to cables.
    """
    list_cableArrangement = ListField(
        StringField,
        required=True
    )
    default_cableArrangement = StringField(
        choices=list_cableArrangement,
        required=True
    )
    list_cableArmour = ListField(
        StringField,
        required=True
    )
    default_cableArmour = StringField(
        choices=list_cableArmour,
        required=True
    )
    list_cableShape = ListField(
        StringField,
        required=True
    )
    default_cableShape = StringField(
        choices=list_cableShape,
        required=True
    )
    list_cableType = ListField(
        StringField,
        required=True
    )
    default_cableType = StringField(
        choices=list_cableType,
        required=True
    )
    list_cableScreen = ListField(
        StringField,
        required=True
    )
    default_cableScreen = StringField(
        choices=list_cableScreen,
        required=True
    )
    list_conductorMaterial = ListField(
        StringField,
        required=True
    )
    default_conductorMaterial = StringField(
        choices=list_conductorMaterial,
        required=True
    )
    list_conductorSize = ListField(
        DecimalField(
            precision=1,
        ),
        required=True
    )
    # Add circuitType to core arrangement to allow the better definition of cables
    list_coreArrangement = ListField(
        StringField,
        required=True
    )
    default_coreArrangement = StringField(
        choices=list_coreArrangement,
        required=True
    )
    list_coreName = ListField(
        StringField,
        required=True
    )
    default_coreName = StringField(
        choices=list_coreName,
        required=True
    )
    list_coreScreen = ListField(
        StringField,
        required=True
    )
    default_coreScreen = StringField(
        choices=list_coreScreen,
        required=True
    )
    list_coreType = ListField(
        StringField,
        required=True
    )
    default_coreType = StringField(
        choices=list_coreType,
        required=True
    )
    list_insulationCode = ListField(
        StringField,
        required=True
    )
    default_insulationCode = StringField(
        choices=list_insulationCode,
        required=True
    )
    list_insulationType = ListField(
        StringField,
        required=True
    )
    default_insulationType = StringField(
        choices=list_insulationType,
        required=True
    )
    list_voltRating = ListField(
        StringField,
        required=True
    )
    default_voltRating = StringField(
        choices=list_voltRating,
        required=True
    )
    default_minCableSize = DecimalField(
        choices=list_conductorSize,
        required=True
    )
    default_minCableSingleCoreSize = DecimalField(
        choices=list_conductorSize,
        required=True
    )
    list_sizeUnit = ListField(
        StringField,
        required=True
    )
    default_sizeUnit = StringField(
        required=True
    )
    list_flexCable = ListField(
        StringField,
        required=True
    )
    default_flexCable = StringField(
        choices=list_flexCable,
        required=True
    )



class DBDefaults(Document):
    """
    Basic default document class, this contains basic information for the variables used.
    """
    cableRunDefault = EmbeddedDocumentField(
        CableRunDefault,
        required=True
    )

    CableDefault = EmbeddedDocumentField(
        CableDefault,
        required=True
    )
    CircuitDefault = EmbeddedDocumentField(
        CircuitDefault,
        required=True
    )



