(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		Plate_24f0b140 - object
		Mug_8e482ae7 - object
		Egg_088cf379 - object
		Toaster_f745e839 - object
		Bread_fe4bb3e3 - object
		LightSwitch_43d10eaa - object
		Floor_1902395b - object
		Lettuce_3b3e7df4 - object
		DiningTable_fc569e38 - object
		Knife_3c40791c - object
		Fridge_22a96a15 - object
		Pot_870f5e0e - object
		Cup_a7567614 - object
		GarbageCan_0d2d5232 - object
		Potato_c28289a1 - object
		Bowl_bd22067b - object
		DiningTable_b56db783 - object
	)
	(:init
		(sliceable Bread_fe4bb3e3)
		(pickupable Bread_fe4bb3e3)
		(temperature Bread_fe4bb3e3 RoomTemp)
		(temperature Bread_fe4bb3e3 Cold)
		(isPlacedAt Bread_fe4bb3e3 Fridge_22a96a15)
		(temperature Fridge_22a96a15 RoomTemp)
		(receptacle Fridge_22a96a15)
		(openable Fridge_22a96a15)
		(isPlacedAt Fridge_22a96a15 Floor_1902395b)
		(isPlacedAt Lettuce_3b3e7df4 Fridge_22a96a15)
		(isPlacedAt Potato_c28289a1 Fridge_22a96a15)
		(isPlacedAt Egg_088cf379 Fridge_22a96a15)
		(isColdSource Fridge_22a96a15)
		(isFridge Fridge_22a96a15)
		(temperature DiningTable_fc569e38 RoomTemp)
		(receptacle DiningTable_fc569e38)
		(isPlacedAt Bowl_bd22067b DiningTable_fc569e38)
		(isPlacedAt Pot_870f5e0e DiningTable_fc569e38)
		(isPlacedAt Cup_a7567614 DiningTable_fc569e38)
		(isPlacedAt DiningTable_fc569e38 Floor_1902395b)
		(pickupable Bowl_bd22067b)
		(temperature Bowl_bd22067b RoomTemp)
		(receptacle Bowl_bd22067b)
		(breakable Bowl_bd22067b)
		(canFillWithLiquid Bowl_bd22067b)
		(dirtyable Bowl_bd22067b)
		(pickupable Pot_870f5e0e)
		(temperature Pot_870f5e0e RoomTemp)
		(receptacle Pot_870f5e0e)
		(canFillWithLiquid Pot_870f5e0e)
		(dirtyable Pot_870f5e0e)
		(pickupable Cup_a7567614)
		(temperature Cup_a7567614 RoomTemp)
		(receptacle Cup_a7567614)
		(breakable Cup_a7567614)
		(canFillWithLiquid Cup_a7567614)
		(dirtyable Cup_a7567614)
		(temperature Floor_1902395b Cold)
		(receptacle Floor_1902395b)
		(isPlacedAt DiningTable_b56db783 Floor_1902395b)
		(isPlacedAt Fridge_22a96a15 Floor_1902395b)
		(isPlacedAt GarbageCan_0d2d5232 Floor_1902395b)
		(temperature DiningTable_b56db783 RoomTemp)
		(receptacle DiningTable_b56db783)
		(isPlacedAt Toaster_f745e839 DiningTable_b56db783)
		(isPlacedAt Knife_3c40791c DiningTable_b56db783)
		(isPlacedAt Plate_24f0b140 DiningTable_b56db783)
		(isPlacedAt Mug_8e482ae7 DiningTable_b56db783)
		(isPlacedAt DiningTable_b56db783 Floor_1902395b)
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
		(dirtyable Mug_8e482ae7)
		(temperature Floor_1902395b Cold)
		(receptacle Floor_1902395b)
		(isPlacedAt Fridge_22a96a15 Floor_1902395b)
		(isPlacedAt DiningTable_fc569e38 Floor_1902395b)
		(isPlacedAt GarbageCan_0d2d5232 Floor_1902395b)
		(atLocation Robot LightSwitch_43d10eaa)
		(temperature LightSwitch_43d10eaa RoomTemp)
		(toggleable LightSwitch_43d10eaa)
		(isToggled LightSwitch_43d10eaa)
		(sliceable Egg_088cf379)
		(pickupable Egg_088cf379)
		(temperature Egg_088cf379 Cold)
		(breakable Egg_088cf379)
		(isPlacedAt Egg_088cf379 Fridge_22a96a15)
		(temperature Fridge_22a96a15 RoomTemp)
		(receptacle Fridge_22a96a15)
		(openable Fridge_22a96a15)
		(isPlacedAt Fridge_22a96a15 Floor_1902395b)
		(isPlacedAt Lettuce_3b3e7df4 Fridge_22a96a15)
		(isPlacedAt Potato_c28289a1 Fridge_22a96a15)
		(isPlacedAt Bread_fe4bb3e3 Fridge_22a96a15)
		(isColdSource Fridge_22a96a15)
		(isFridge Fridge_22a96a15)
		(sliceable Potato_c28289a1)
		(pickupable Potato_c28289a1)
		(temperature Potato_c28289a1 RoomTemp)
		(isPlacedAt Potato_c28289a1 Fridge_22a96a15)
		(cookable Potato_c28289a1)
		(temperature Fridge_22a96a15 RoomTemp)
		(receptacle Fridge_22a96a15)
		(openable Fridge_22a96a15)
		(isPlacedAt Fridge_22a96a15 Floor_1902395b)
		(isPlacedAt Lettuce_3b3e7df4 Fridge_22a96a15)
		(isPlacedAt Egg_088cf379 Fridge_22a96a15)
		(isPlacedAt Bread_fe4bb3e3 Fridge_22a96a15)
		(isColdSource Fridge_22a96a15)
		(isFridge Fridge_22a96a15)
	)
	(:goal (and
    (isPlacedAt Potato_c28289a1 DiningTable_fc569e38)
    (isPlacedAt Bread_fe4bb3e3 DiningTable_fc569e38)
    (isPlacedAt Egg_088cf379 DiningTable_fc569e38)
))
)