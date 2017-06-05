# Electrical equipment list

Tag = StringField(
    unique=True
    )

	<!--
    - Base on:

		1. Parent Equipment
		2. Equipment Type
		3. Unique Identifier

			- This can be unique to equipment type, or as a global value

	- Able to be modified if the parent equipment changes.
    -->

Description = StringField()
	<!--
	- Derived from:

		1. Equipment Type
		2. Parent Equipment
		3. Unique identifier
		4. User input description(?)
		5. Location
		 -->

3.	Equipment Layout Drawing Number

	- TEXT STRING

Location = StringField()
<!--
    - Determined from predefined list
	    - TblLocation
    - This is a process area location
    -->

Contract.Supply = StringField()
<!--
    - Determined from predefined list
	    - TblSupplyPackage
        -->

Contract.Installation = StringField()
<!--
	- Determined from predefined list
	    - TblInstallPackage
	    -->

Contract.Connect = StringField()
<!--
	- Determined from predefined list
	    - TblConnectPackage
        -->

8. Reference Drawing Number

	- TEXT STRING

Comments = StringField()
<!--
	- TEXT STRING (enumerated)
	- Separate Table
	    - TblEquipmentListComments
    -->

EquipType = StringField(
    choices = <EquipType List>
    )
<!--
	- Determined from predefined list
	    - TblEquipType
    -->

DataSheet = ReferenceField()
<!--
	- Refers to DataSheet collection
    -->

Circuit.Voltage = IntField(
        required=True,
        choices=cableVar.list_circuitVoltage
    )

Circuit.P = IntField()
<!--
    - This is kW
    -->

Circuit.S = IntField()
<!--
    - This is kVA
    -->

Circuit.Q = IntField()
<!--
    - This is kVAr
    -->

Rev.Number = StringField()
<!--
	- AUTO GENERATED
	- Autoupdated when a field is changed.
    -->
