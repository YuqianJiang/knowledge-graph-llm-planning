(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		Cabinet_6dd6babd - object
		Cabinet_78f721d5 - object
		Cabinet_69241a54 - object
		CounterTop_319feff1 - object
		CoffeeMachine_ce92cf84 - object
		SinkBasin_25ff5803 - object
		PepperShaker_ef77f99c - object
		DishSponge_a2e8b0f9 - object
		Cabinet_47fc321b - object
		Cabinet_796e4b24 - object
		StoveKnob_690d0d5d - object
		StoveBurner_1253da28 - object
		Pan_9ab103d1 - object
		Cabinet_53903f72 - object
		SaltShaker_4e4b3565 - object
		Mug_2ec601ad - object
	)
	(:init
		(temperature Cabinet_6dd6babd RoomTemp)
		(receptacle Cabinet_6dd6babd)
		(openable Cabinet_6dd6babd)
		(temperature Cabinet_69241a54 RoomTemp)
		(receptacle Cabinet_69241a54)
		(openable Cabinet_69241a54)
		(temperature CounterTop_319feff1 RoomTemp)
		(receptacle CounterTop_319feff1)
		(isPlacedAt SaltShaker_4e4b3565 CounterTop_319feff1)
		(isPlacedAt PepperShaker_ef77f99c CounterTop_319feff1)
		(isPlacedAt CoffeeMachine_ce92cf84 CounterTop_319feff1)
		(pickupable SaltShaker_4e4b3565)
		(temperature SaltShaker_4e4b3565 RoomTemp)
		(pickupable PepperShaker_ef77f99c)
		(temperature PepperShaker_ef77f99c RoomTemp)
		(temperature CoffeeMachine_ce92cf84 RoomTemp)
		(receptacle CoffeeMachine_ce92cf84)
		(toggleable CoffeeMachine_ce92cf84)
		(isHeatSource CoffeeMachine_ce92cf84)
		(temperature SinkBasin_25ff5803 RoomTemp)
		(receptacle SinkBasin_25ff5803)
		(isPlacedAt DishSponge_a2e8b0f9 SinkBasin_25ff5803)
		(isPlacedAt Mug_2ec601ad SinkBasin_25ff5803)
		(isSinkBasin SinkBasin_25ff5803)
		(pickupable DishSponge_a2e8b0f9)
		(temperature DishSponge_a2e8b0f9 RoomTemp)
		(pickupable Mug_2ec601ad)
		(temperature Mug_2ec601ad RoomTemp)
		(breakable Mug_2ec601ad)
		(canFillWithLiquid Mug_2ec601ad)
		(receptacle Mug_2ec601ad)
		(dirtyable Mug_2ec601ad)
		(isDirty Mug_2ec601ad)
		(temperature Cabinet_47fc321b RoomTemp)
		(receptacle Cabinet_47fc321b)
		(openable Cabinet_47fc321b)
		(temperature Cabinet_796e4b24 RoomTemp)
		(receptacle Cabinet_796e4b24)
		(openable Cabinet_796e4b24)
		(temperature Cabinet_53903f72 RoomTemp)
		(receptacle Cabinet_53903f72)
		(openable Cabinet_53903f72)
		(temperature Cabinet_78f721d5 RoomTemp)
		(receptacle Cabinet_78f721d5)
		(openable Cabinet_78f721d5)
		(atLocation Robot StoveBurner_1253da28)
		(temperature StoveBurner_1253da28 RoomTemp)
		(controlledObjects StoveKnob_690d0d5d StoveBurner_1253da28)
		(receptacle StoveBurner_1253da28)
		(isHeatSource StoveBurner_1253da28)
		(isPlacedAt Pan_9ab103d1 StoveBurner_1253da28)
		(pickupable DishSponge_a2e8b0f9)
		(temperature DishSponge_a2e8b0f9 RoomTemp)
		(isPlacedAt DishSponge_a2e8b0f9 SinkBasin_25ff5803)
		(temperature SinkBasin_25ff5803 RoomTemp)
		(receptacle SinkBasin_25ff5803)
		(isPlacedAt Mug_2ec601ad SinkBasin_25ff5803)
		(isSinkBasin SinkBasin_25ff5803)
	)
	(:goal (and
    (not (isDirty SaltShaker_4e4b3565))
    (not (isDirty PepperShaker_ef77f99c))
    (not (isDirty CoffeeMachine_ce92cf84))
    (not (isDirty DishSponge_a2e8b0f9))
    (not (isDirty Mug_2ec601ad))
))
)