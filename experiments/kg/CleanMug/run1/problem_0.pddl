(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		SaltShaker_aa7ee03f - object
		Microwave_e71f2758 - object
		SoapBottle_76711a6f - object
		LightSwitch_43d10eaa - object
		Spatula_7afbb68f - object
		CounterTop_0aab7a9f - object
		SinkBasin_ad9ebd80 - object
		ButterKnife_9d61f327 - object
		PepperShaker_ca490222 - object
		CounterTop_8700c90d - object
		Tomato_f8bc52bb - object
		Mug_8e482ae7 - object
		Faucet_41abd2a0 - object
		DishSponge_c51474f6 - object
		Apple_499e3527 - object
		CoffeeMachine_61ed6a3e - object
	)
	(:init
		(temperature SinkBasin_ad9ebd80 RoomTemp)
		(receptacle SinkBasin_ad9ebd80)
		(isPlacedAt DishSponge_c51474f6 SinkBasin_ad9ebd80)
		(isPlacedAt Tomato_f8bc52bb SinkBasin_ad9ebd80)
		(isPlacedAt CounterTop_0aab7a9f SinkBasin_ad9ebd80)
		(isSinkBasin SinkBasin_ad9ebd80)
		(pickupable DishSponge_c51474f6)
		(temperature DishSponge_c51474f6 RoomTemp)
		(sliceable Tomato_f8bc52bb)
		(pickupable Tomato_f8bc52bb)
		(temperature Tomato_f8bc52bb RoomTemp)
		(temperature CounterTop_0aab7a9f RoomTemp)
		(receptacle CounterTop_0aab7a9f)
		(isPlacedAt Apple_499e3527 CounterTop_0aab7a9f)
		(isPlacedAt SoapBottle_76711a6f CounterTop_0aab7a9f)
		(isPlacedAt PepperShaker_ca490222 CounterTop_0aab7a9f)
		(isPlacedAt SaltShaker_aa7ee03f CounterTop_0aab7a9f)
		(isPlacedAt ButterKnife_9d61f327 CounterTop_0aab7a9f)
		(isPlacedAt Spatula_7afbb68f CounterTop_0aab7a9f)
		(isPlacedAt Microwave_e71f2758 CounterTop_0aab7a9f)
		(isPlacedAt Faucet_41abd2a0 CounterTop_0aab7a9f)
		(pickupable Mug_8e482ae7)
		(temperature Mug_8e482ae7 RoomTemp)
		(receptacle Mug_8e482ae7)
		(breakable Mug_8e482ae7)
		(canFillWithLiquid Mug_8e482ae7)
		(dirtyable Mug_8e482ae7)
		(isPlacedAt Mug_8e482ae7 CoffeeMachine_61ed6a3e)
		(temperature CoffeeMachine_61ed6a3e RoomTemp)
		(receptacle CoffeeMachine_61ed6a3e)
		(toggleable CoffeeMachine_61ed6a3e)
		(isHeatSource CoffeeMachine_61ed6a3e)
		(isPlacedAt CoffeeMachine_61ed6a3e CounterTop_8700c90d)
		(atLocation Robot LightSwitch_43d10eaa)
		(temperature LightSwitch_43d10eaa RoomTemp)
		(toggleable LightSwitch_43d10eaa)
		(isToggled LightSwitch_43d10eaa)
	)
	(:goal (and
    (isPlacedAt Mug_8e482ae7 DiningTable)
    (not (isDirty Mug_8e482ae7))
))
)