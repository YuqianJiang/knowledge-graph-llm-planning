(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		Pot_870f5e0e - object
		Plate_24f0b140 - object
		Microwave_e71f2758 - object
		DiningTable_b56db783 - object
		SaltShaker_aa7ee03f - object
		Apple_499e3527 - object
		CounterTop_8700c90d - object
		SinkBasin_ad9ebd80 - object
		Knife_3c40791c - object
		DiningTable_fc569e38 - object
		SoapBottle_76711a6f - object
		Bread_fe4bb3e3 - object
		Mug_8e482ae7 - object
		CoffeeMachine_61ed6a3e - object
		ButterKnife_9d61f327 - object
		PepperShaker_ca490222 - object
		Bowl_bd22067b - object
		Toaster_f745e839 - object
		LightSwitch_43d10eaa - object
		CounterTop_0aab7a9f - object
		DishSponge_c51474f6 - object
		Cup_a7567614 - object
		Faucet_41abd2a0 - object
		Spatula_7afbb68f - object
		Tomato_f8bc52bb - object
	)
	(:init
		(isPlacedAt Knife_3c40791c DiningTable_b56db783)
		(isPlacedAt Plate_24f0b140 DiningTable_b56db783)
		(isPlacedAt Toaster_f745e839 DiningTable_b56db783)
		(temperature DiningTable_b56db783 RoomTemp)
		(receptacle DiningTable_b56db783)
		(pickupable Knife_3c40791c)
		(temperature Knife_3c40791c RoomTemp)
		(pickupable Plate_24f0b140)
		(temperature Plate_24f0b140 RoomTemp)
		(receptacle Plate_24f0b140)
		(breakable Plate_24f0b140)
		(dirtyable Plate_24f0b140)
		(temperature Toaster_f745e839 RoomTemp)
		(receptacle Toaster_f745e839)
		(toggleable Toaster_f745e839)
		(isHeatSource Toaster_f745e839)
		(isPlacedAt CounterTop_0aab7a9f SinkBasin_ad9ebd80)
		(isPlacedAt DishSponge_c51474f6 SinkBasin_ad9ebd80)
		(isPlacedAt Tomato_f8bc52bb SinkBasin_ad9ebd80)
		(temperature SinkBasin_ad9ebd80 RoomTemp)
		(receptacle SinkBasin_ad9ebd80)
		(isSinkBasin SinkBasin_ad9ebd80)
		(isPlacedAt Apple_499e3527 CounterTop_0aab7a9f)
		(isPlacedAt ButterKnife_9d61f327 CounterTop_0aab7a9f)
		(isPlacedAt Faucet_41abd2a0 CounterTop_0aab7a9f)
		(isPlacedAt Microwave_e71f2758 CounterTop_0aab7a9f)
		(isPlacedAt PepperShaker_ca490222 CounterTop_0aab7a9f)
		(isPlacedAt SaltShaker_aa7ee03f CounterTop_0aab7a9f)
		(isPlacedAt SoapBottle_76711a6f CounterTop_0aab7a9f)
		(isPlacedAt Spatula_7afbb68f CounterTop_0aab7a9f)
		(isInteractable CounterTop_0aab7a9f)
		(temperature CounterTop_0aab7a9f RoomTemp)
		(receptacle CounterTop_0aab7a9f)
		(pickupable DishSponge_c51474f6)
		(temperature DishSponge_c51474f6 RoomTemp)
		(sliceable Tomato_f8bc52bb)
		(pickupable Tomato_f8bc52bb)
		(temperature Tomato_f8bc52bb RoomTemp)
		(isPlacedAt Bowl_bd22067b DiningTable_fc569e38)
		(isPlacedAt Bread_fe4bb3e3 DiningTable_fc569e38)
		(isPlacedAt Cup_a7567614 DiningTable_fc569e38)
		(isPlacedAt Pot_870f5e0e DiningTable_fc569e38)
		(temperature DiningTable_fc569e38 RoomTemp)
		(receptacle DiningTable_fc569e38)
		(pickupable Bowl_bd22067b)
		(temperature Bowl_bd22067b RoomTemp)
		(receptacle Bowl_bd22067b)
		(breakable Bowl_bd22067b)
		(canFillWithLiquid Bowl_bd22067b)
		(dirtyable Bowl_bd22067b)
		(sliceable Bread_fe4bb3e3)
		(pickupable Bread_fe4bb3e3)
		(temperature Bread_fe4bb3e3 RoomTemp)
		(pickupable Cup_a7567614)
		(temperature Cup_a7567614 RoomTemp)
		(receptacle Cup_a7567614)
		(breakable Cup_a7567614)
		(canFillWithLiquid Cup_a7567614)
		(dirtyable Cup_a7567614)
		(pickupable Pot_870f5e0e)
		(temperature Pot_870f5e0e RoomTemp)
		(receptacle Pot_870f5e0e)
		(canFillWithLiquid Pot_870f5e0e)
		(dirtyable Pot_870f5e0e)
		(atLocation Robot LightSwitch_43d10eaa)
		(isInteractable LightSwitch_43d10eaa)
		(temperature LightSwitch_43d10eaa RoomTemp)
		(toggleable LightSwitch_43d10eaa)
		(isToggled LightSwitch_43d10eaa)
		(pickupable Mug_8e482ae7)
		(isPlacedAt Mug_8e482ae7 CoffeeMachine_61ed6a3e)
		(temperature Mug_8e482ae7 RoomTemp)
		(receptacle Mug_8e482ae7)
		(breakable Mug_8e482ae7)
		(canFillWithLiquid Mug_8e482ae7)
		(dirtyable Mug_8e482ae7)
		(isDirty Mug_8e482ae7)
		(isPlacedAt CoffeeMachine_61ed6a3e CounterTop_8700c90d)
		(temperature CoffeeMachine_61ed6a3e RoomTemp)
		(receptacle CoffeeMachine_61ed6a3e)
		(toggleable CoffeeMachine_61ed6a3e)
		(isHeatSource CoffeeMachine_61ed6a3e)
	)
	(:goal (and
    (isPlacedAt Mug_8e482ae7 DiningTable_b56db783)
    (not (isDirty Mug_8e482ae7))
))
)