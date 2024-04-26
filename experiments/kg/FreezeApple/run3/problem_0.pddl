(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		HousePlant_b9508896 - object
		Bread_5dd97b2d - object
		SoapBottle_5ec2e889 - object
		Plate_49b95a7a - object
		StoveKnob_690d0d5d - object
		CreditCard_fad504dd - object
		Fork_b9c0113d - object
		Apple_f33eaaa0 - object
		Potato_e4559da4 - object
		Egg_afaaaca3 - object
		CounterTop_f036610b - object
		Pot_83694083 - object
		Fridge_5134d575 - object
		Pan_9ab103d1 - object
		ButterKnife_42394ea7 - object
		StoveBurner_1253da28 - object
		Spoon_4a610c23 - object
		Statue_ed6ce732 - object
		Lettuce_0340e5ea - object
		Tomato_9c51c4ef - object
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
		(atLocation Robot StoveBurner_1253da28)
		(temperature StoveBurner_1253da28 RoomTemp)
		(controlledObjects StoveKnob_690d0d5d StoveBurner_1253da28)
		(receptacle StoveBurner_1253da28)
		(isHeatSource StoveBurner_1253da28)
		(isPlacedAt Pan_9ab103d1 StoveBurner_1253da28)
		(sliceable Apple_f33eaaa0)
		(pickupable Apple_f33eaaa0)
		(temperature Apple_f33eaaa0 RoomTemp)
		(isPlacedAt Apple_f33eaaa0 CounterTop_f036610b)
		(temperature CounterTop_f036610b RoomTemp)
		(receptacle CounterTop_f036610b)
		(isPlacedAt Statue_ed6ce732 CounterTop_f036610b)
		(isPlacedAt CreditCard_fad504dd CounterTop_f036610b)
		(isPlacedAt Pot_83694083 CounterTop_f036610b)
		(isPlacedAt Spoon_4a610c23 CounterTop_f036610b)
		(isPlacedAt ButterKnife_42394ea7 CounterTop_f036610b)
		(isPlacedAt Fork_b9c0113d CounterTop_f036610b)
		(isPlacedAt HousePlant_b9508896 CounterTop_f036610b)
		(isPlacedAt SoapBottle_5ec2e889 CounterTop_f036610b)
		(isPlacedAt Plate_49b95a7a CounterTop_f036610b)
		(isPlacedAt Bread_5dd97b2d CounterTop_f036610b)
		(isPlacedAt Potato_e4559da4 CounterTop_f036610b)
		(isPlacedAt Tomato_9c51c4ef CounterTop_f036610b)
	)
	(:goal (and
    (isPlacedAt Apple_f33eaaa0 Fridge_5134d575)
    (temperature Apple_f33eaaa0 Cold)
))
)