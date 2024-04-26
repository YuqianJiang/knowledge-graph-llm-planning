(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		TennisRacket_711cdee9 - object
		Chair_74b9cd06 - object
		TeddyBear_7f283eb8 - object
		Floor_3e4c5de1 - object
		Desk_5980b1e1 - object
		Bed_bef46c99 - object
		CellPhone_f2c48336 - object
		Cloth_4b47e1f9 - object
		BaseballBat_ef1b0e6e - object
		GarbageCan_6fd936bc - object
		Drawer_385dbca5 - object
		Chair_b37e67b5 - object
		Bed_860b294e - object
		Pillow_11419468 - object
		BasketBall_bb2afb95 - object
		SideTable_9daa0f0e - object
	)
	(:init
		(pickupable CellPhone_f2c48336)
		(temperature CellPhone_f2c48336 RoomTemp)
		(isPlacedAt CellPhone_f2c48336 Bed_bef46c99)
		(breakable CellPhone_f2c48336)
		(toggleable CellPhone_f2c48336)
		(temperature Bed_bef46c99 RoomTemp)
		(receptacle Bed_bef46c99)
		(isPlacedAt Pillow_11419468 Bed_bef46c99)
		(isPlacedAt TeddyBear_7f283eb8 Bed_bef46c99)
		(isPlacedAt Bed_bef46c99 Floor_3e4c5de1)
		(dirtyable Bed_bef46c99)
		(isDirty Bed_bef46c99)
		(atLocation Robot Floor_3e4c5de1)
		(temperature Floor_3e4c5de1 RoomTemp)
		(receptacle Floor_3e4c5de1)
		(isPlacedAt Cloth_4b47e1f9 Floor_3e4c5de1)
		(isPlacedAt Bed_860b294e Floor_3e4c5de1)
		(isPlacedAt Drawer_385dbca5 Floor_3e4c5de1)
		(isPlacedAt SideTable_9daa0f0e Floor_3e4c5de1)
		(isPlacedAt Bed_bef46c99 Floor_3e4c5de1)
		(isPlacedAt BaseballBat_ef1b0e6e Floor_3e4c5de1)
		(isPlacedAt TennisRacket_711cdee9 Floor_3e4c5de1)
		(isPlacedAt BasketBall_bb2afb95 Floor_3e4c5de1)
		(isPlacedAt Chair_74b9cd06 Floor_3e4c5de1)
		(isPlacedAt Desk_5980b1e1 Floor_3e4c5de1)
		(isPlacedAt Chair_b37e67b5 Floor_3e4c5de1)
		(isPlacedAt GarbageCan_6fd936bc Floor_3e4c5de1)
		(temperature GarbageCan_6fd936bc RoomTemp)
		(receptacle GarbageCan_6fd936bc)
		(isPlacedAt GarbageCan_6fd936bc Floor_3e4c5de1)
		(temperature Floor_3e4c5de1 RoomTemp)
		(receptacle Floor_3e4c5de1)
		(isPlacedAt Cloth_4b47e1f9 Floor_3e4c5de1)
		(isPlacedAt Bed_860b294e Floor_3e4c5de1)
		(isPlacedAt Drawer_385dbca5 Floor_3e4c5de1)
		(isPlacedAt SideTable_9daa0f0e Floor_3e4c5de1)
		(isPlacedAt Bed_bef46c99 Floor_3e4c5de1)
		(isPlacedAt BaseballBat_ef1b0e6e Floor_3e4c5de1)
		(isPlacedAt TennisRacket_711cdee9 Floor_3e4c5de1)
		(isPlacedAt BasketBall_bb2afb95 Floor_3e4c5de1)
		(isPlacedAt Chair_74b9cd06 Floor_3e4c5de1)
		(isPlacedAt Desk_5980b1e1 Floor_3e4c5de1)
		(isPlacedAt Chair_b37e67b5 Floor_3e4c5de1)
		(atLocation Robot Floor_3e4c5de1)
	)
	(:goal (and
    (isPlacedAt CellPhone_f2c48336 GarbageCan_6fd936bc)
))
)