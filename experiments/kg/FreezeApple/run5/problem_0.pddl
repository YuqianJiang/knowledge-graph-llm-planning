(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		Microwave_d8b935e4 - object
		Apple_f33eaaa0 - object
		Lettuce_0340e5ea - object
		StoveKnob_690d0d5d - object
		Fridge_5134d575 - object
		Egg_afaaaca3 - object
		StoveBurner_1253da28 - object
		Pan_9ab103d1 - object
	)
	(:init
		(temperature Fridge_5134d575 RoomTemp)
		(receptacle Fridge_5134d575)
		(openable Fridge_5134d575)
		(isPlacedAt Egg_afaaaca3 Fridge_5134d575)
		(isPlacedAt Lettuce_0340e5ea Fridge_5134d575)
		(isColdSource Fridge_5134d575)
		(isFridge Fridge_5134d575)
		(sliceable Egg_afaaaca3)
		(pickupable Egg_afaaaca3)
		(temperature Egg_afaaaca3 Cold)
		(breakable Egg_afaaaca3)
		(sliceable Lettuce_0340e5ea)
		(pickupable Lettuce_0340e5ea)
		(temperature Lettuce_0340e5ea Cold)
		(sliceable Apple_f33eaaa0)
		(pickupable Apple_f33eaaa0)
		(temperature Apple_f33eaaa0 RoomTemp)
		(isPlacedAt Apple_f33eaaa0 Microwave_d8b935e4)
		(temperature Microwave_d8b935e4 RoomTemp)
		(receptacle Microwave_d8b935e4)
		(openable Microwave_d8b935e4)
		(toggleable Microwave_d8b935e4)
		(isHeatSource Microwave_d8b935e4)
		(isMicrowave Microwave_d8b935e4)
		(atLocation Robot StoveBurner_1253da28)
		(temperature StoveBurner_1253da28 RoomTemp)
		(controlledObjects StoveKnob_690d0d5d StoveBurner_1253da28)
		(receptacle StoveBurner_1253da28)
		(isHeatSource StoveBurner_1253da28)
		(isPlacedAt Pan_9ab103d1 StoveBurner_1253da28)
	)
	(:goal (and
    (isPlacedAt Apple_f33eaaa0 Fridge_5134d575)
    (temperature Apple_f33eaaa0 Cold)
))
)