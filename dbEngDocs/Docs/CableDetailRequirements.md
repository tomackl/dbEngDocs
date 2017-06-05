
#### cableType

This deals with the electrical function of the cable, in the case of power cables whether it is an active, neutral or earth conductor. Other cable such as comms and data cables are also allowed for.

`ACTIVE` An active cable. Includes single- and multi-core cables. Where it is a single core cable it represents an active conductor of a single core cable circuit.

`NEUTRAL` A neutral conductor or cable. Usually limited to single core cables.

`EARTH` An earth cable or conductor.

`CONTROL` A control cable.

`INSTRUMENT` An instrumenation cable.

`DATA` A data cable.

`COMMS` A comms cable.

#### cableShape

The shape of the cable. This has no functional purpose but allows for installation or specification requirements.

`CIRCULAR` The cable has a circular cross section.

`FLAT` The cable has a flat cross section.

#### circuitType

Defines what circuit of circuit that the cable will be feeding.

`SINGLE` The cable characteristics are based on a single phase circuit.

`MULTI` The cable characteristics are based on a multi-phase circuit.

`CONTROL` The cable is used for control circuits. (That is, digital control circuits).

`INSTRUMENT` Instrumentation cable. Intended for 4-20mA circuits.

`COMMS` Communication cables.

`DATA` Data cable e.g. Cat 6, Profibus, etc.


#### conductorMaterial

The material that the cable conductors are manufactured from.

`CU` Copper

`AL` Aluminium

#### installMethod

Generally as per the AS3008.1.1 definitions.

`UNENCLOSED_SPACED`

`UNENCLOSED_SURFACE`

`UNENCLOSED_TOUCHING`

`ENCLOSED_CONDUIT`

`ENCLOSED_PARTIAL`

`ENCLOSED_COMPLETE`

`UNENCLOSED_PARTIAL`

`UNENCLOSED_COMPLETE`

`BURIED_DIRECT`

`UNDERGROUND_DUCTS`

`DUCTS_SINGLE`

`DUCTS_PER_CABLE`

#### cableArrangement

Only associated with single core cables. Addresses the arrangement of the cores in a multi-phase circuit runs and the related current carrying capacity of the cable.

`NIL`

`FLAT`

`TREFOIL`

#### sheathType

The material that the cable sheath is manufactured from.

`PVC` Polyvinyl chloride.

`HDPE` High-density polyethylene.

`EPR`

`UNSHEATHED`

#### insulationType

Cable insulation type.

`XLPE` Cross-linked polyethylene.

`PVC` Polyvinyl chloride.

`PILS` Paper insulated lead sheath.

`EPR` Rubber.

#### insulationCode

`X-90` XLPE. 90dC maximum temperature.

`V-90` PVC high temp. 90dC maximum temperature.

`V-90RP`

`V-75` PVC 70dC maximum temperature.

#### voltRating

`300/500V` Single/multi-phase insulation voltage.

`450/750V` Single/multi-phase insulation voltage.

`110V` Single insulation voltage.

`0.6/1KV` Single/multi-phase insulation voltage.

`12.7/22KV` Single/multi-phase insulation voltage.

`6.35/11KV` Single/multi-phase insulation voltage.

#### circuitVoltage

Voltage of the circuit. Use with the `circuitCurrent`.

`24`

`48`

`110`

`240`

`415`

`1000`

#### circuitCurrent

`AC` Alternating current.

`DC` Direct current.

#### conductorSize

Conductor cross sectional area.

`0`

`1`

`1.5`

`2.5`

`4`

`6`

`10`

`16`

`25`

`35`

`50`

`70`

`95`

`120`

`150`

`185`

`240`

`300`

`400`

`500`

`630`

#### sizeUnit

`MM2`


#### coreArrangements

The following a cable core arrangements.

`-`

`1C`

`2C`

`3C`

`2C+E`

`3C+E`

`3C+3E`

`4C+E`

`2C+E`

`4C+E`

`5C+E`

`10C+E`

`20C+E`

`50C+E`

`1PR`

`2PR`

`4PR`

`5PR`

`6PR`

`10PR`

`12PR`

`20PR`

`1TRI`

`2TRI`

`4TRI`

`5TRI`

`6TRI`

`10TRI`

`12TRI`

`20TRI`

#### cableArmour

`NIL` No armouring.

`SWA` Steel wire armour.

`DWA` Dual wire armour.

#### CableScreen

`NIL` No cable screen.

`DCT` Double copper tape.

`OS` Overall screen.

#### CoreScreen

`NIL` No cable screen.

`IS` Individual screen.

#### power

`WATTS: 1`

`W: 1`

`KILO-WATT: 1000`

`KW: 1000`

`VOLT-AMPS: 1`

`VA: 1`

`KILO-VOLT-AMPS: 1000`

`KVA: 1000`

#### flexCable

Is the cable flexible.

`TRUE`

`FALSE`
