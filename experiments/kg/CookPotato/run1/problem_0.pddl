(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		StoveBurner_1253da28 - object
		StoveKnob_690d0d5d - object
		Potato_e4559da4 - object
		Egg_afaaaca3 - object
		Microwave_d8b935e4 - object
		Lettuce_0340e5ea - object
		Pan_9ab103d1 - object
		Fridge_5134d575 - object
	)
	(:init
		(atLocation Robot StoveBurner_1253da28)
		(temperature StoveBurner_1253da28 RoomTemp)
		(controlledObjects StoveKnob_690d0d5d StoveBurner_1253da28)
		(receptacle StoveBurner_1253da28)
		(isHeatSource StoveBurner_1253da28)
		(isPlacedAt Pan_9ab103d1 StoveBurner_1253da28)
		(sliceable Potato_e4559da4)
		(pickupable Potato_e4559da4)
		(temperature Potato_e4559da4 RoomTemp)
		(isPlacedAt Potato_e4559da4 Fridge_5134d575)
		(cookable Potato_e4559da4)
		(temperature Fridge_5134d575 RoomTemp)
		(receptacle Fridge_5134d575)
		(openable Fridge_5134d575)
		(isPlacedAt Egg_afaaaca3 Fridge_5134d575)
		(isPlacedAt Lettuce_0340e5ea Fridge_5134d575)
		(isColdSource Fridge_5134d575)
		(isFridge Fridge_5134d575)
		(temperature Microwave_d8b935e4 RoomTemp)
		(receptacle Microwave_d8b935e4)
		(openable Microwave_d8b935e4)
		(toggleable Microwave_d8b935e4)
		(isHeatSource Microwave_d8b935e4)
		(isMicrowave Microwave_d8b935e4)
	)
	(:goal (and
    (temperature Potato_e4559da4 Hot)
))
)