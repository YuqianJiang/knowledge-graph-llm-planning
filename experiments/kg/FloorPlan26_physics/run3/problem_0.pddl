(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		Potato_c28289a1 - object
		Mug_8e482ae7 - object
		CoffeeMachine_61ed6a3e - object
		coffee - object
		CounterTop_8700c90d - object
		Knife_3c40791c - object
		LightSwitch_43d10eaa - object
		DiningTable_b56db783 - object
		Plate_24f0b140 - object
		Toaster_f745e839 - object
	)
	(:init
		(temperature CoffeeMachine_61ed6a3e RoomTemp)
		(receptacle CoffeeMachine_61ed6a3e)
		(toggleable CoffeeMachine_61ed6a3e)
		(isHeatSource CoffeeMachine_61ed6a3e)
		(isPlacedAt CoffeeMachine_61ed6a3e CounterTop_8700c90d)
		(isPlacedAt Mug_8e482ae7 CoffeeMachine_61ed6a3e)
		(temperature CounterTop_8700c90d RoomTemp)
		(receptacle CounterTop_8700c90d)
		(isPlacedAt Potato_c28289a1 CounterTop_8700c90d)
		(pickupable Mug_8e482ae7)
		(temperature Mug_8e482ae7 RoomTemp)
		(receptacle Mug_8e482ae7)
		(breakable Mug_8e482ae7)
		(canFillWithLiquid Mug_8e482ae7)
		(isFilledWithLiquid Mug_8e482ae7)
		(fillLiquid Mug_8e482ae7 coffee)
		(dirtyable Mug_8e482ae7)
		(temperature DiningTable_b56db783 RoomTemp)
		(receptacle DiningTable_b56db783)
		(isPlacedAt Toaster_f745e839 DiningTable_b56db783)
		(isPlacedAt Knife_3c40791c DiningTable_b56db783)
		(isPlacedAt Plate_24f0b140 DiningTable_b56db783)
		(temperature Toaster_f745e839 RoomTemp)
		(receptacle Toaster_f745e839)
		(toggleable Toaster_f745e839)
		(isHeatSource Toaster_f745e839)
		(pickupable Knife_3c40791c)
		(temperature Knife_3c40791c RoomTemp)
		(pickupable Plate_24f0b140)
		(temperature Plate_24f0b140 RoomTemp)
		(receptacle Plate_24f0b140)
		(breakable Plate_24f0b140)
		(dirtyable Plate_24f0b140)
		(pickupable Mug_8e482ae7)
		(temperature Mug_8e482ae7 RoomTemp)
		(receptacle Mug_8e482ae7)
		(breakable Mug_8e482ae7)
		(canFillWithLiquid Mug_8e482ae7)
		(isFilledWithLiquid Mug_8e482ae7)
		(fillLiquid Mug_8e482ae7 coffee)
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
    (isPlacedAt Mug_8e482ae7 DiningTable_b56db783)
    (fillLiquid Mug_8e482ae7 Coffee)
))
)