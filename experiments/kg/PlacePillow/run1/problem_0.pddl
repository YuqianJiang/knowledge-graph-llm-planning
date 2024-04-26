(define (problem p0)
	(:domain robot)
	(:objects
		Robot - robot
		Pillow_0c062a19 - object
		Floor_9ce8d4dd - object
		Drawer_c1b1c71e - object
		Dresser_51c303cb - object
		Sofa_b5903624 - object
		Drawer_d857444d - object
		SideTable_b82ed100 - object
		Bed_b8ad3dcc - object
		Drawer_9950548b - object
		SideTable_a9b9b711 - object
		Laptop_f57c484a - object
		Desk_8c41b1c0 - object
		GarbageCan_92106b41 - object
		Chair_a3bee7ce - object
		TeddyBear_cde4a75b - object
		Drawer_03580458 - object
		Pillow_974691ae - object
	)
	(:init
		(pickupable Pillow_0c062a19)
		(temperature Pillow_0c062a19 RoomTemp)
		(isPlacedAt Pillow_0c062a19 Sofa_b5903624)
		(temperature Sofa_b5903624 RoomTemp)
		(receptacle Sofa_b5903624)
		(isPlacedAt Sofa_b5903624 Floor_9ce8d4dd)
		(atLocation Robot Floor_9ce8d4dd)
		(temperature Floor_9ce8d4dd RoomTemp)
		(receptacle Floor_9ce8d4dd)
		(isPlacedAt Dresser_51c303cb Floor_9ce8d4dd)
		(isPlacedAt Drawer_d857444d Floor_9ce8d4dd)
		(isPlacedAt Sofa_b5903624 Floor_9ce8d4dd)
		(isPlacedAt Desk_8c41b1c0 Floor_9ce8d4dd)
		(isPlacedAt Drawer_c1b1c71e Floor_9ce8d4dd)
		(isPlacedAt GarbageCan_92106b41 Floor_9ce8d4dd)
		(isPlacedAt Chair_a3bee7ce Floor_9ce8d4dd)
		(isPlacedAt Bed_b8ad3dcc Floor_9ce8d4dd)
		(isPlacedAt Drawer_9950548b Floor_9ce8d4dd)
		(isPlacedAt SideTable_a9b9b711 Floor_9ce8d4dd)
		(isPlacedAt SideTable_b82ed100 Floor_9ce8d4dd)
		(isPlacedAt Drawer_03580458 Floor_9ce8d4dd)
		(temperature Bed_b8ad3dcc RoomTemp)
		(receptacle Bed_b8ad3dcc)
		(isPlacedAt Pillow_974691ae Bed_b8ad3dcc)
		(isPlacedAt Laptop_f57c484a Bed_b8ad3dcc)
		(isPlacedAt TeddyBear_cde4a75b Bed_b8ad3dcc)
		(isPlacedAt Bed_b8ad3dcc Floor_9ce8d4dd)
		(dirtyable Bed_b8ad3dcc)
		(isDirty Bed_b8ad3dcc)
		(pickupable Pillow_974691ae)
		(temperature Pillow_974691ae RoomTemp)
		(pickupable Laptop_f57c484a)
		(temperature Laptop_f57c484a RoomTemp)
		(openable Laptop_f57c484a)
		(isOpen Laptop_f57c484a)
		(breakable Laptop_f57c484a)
		(toggleable Laptop_f57c484a)
		(pickupable TeddyBear_cde4a75b)
		(temperature TeddyBear_cde4a75b RoomTemp)
		(temperature Floor_9ce8d4dd RoomTemp)
		(receptacle Floor_9ce8d4dd)
		(isPlacedAt Dresser_51c303cb Floor_9ce8d4dd)
		(isPlacedAt Drawer_d857444d Floor_9ce8d4dd)
		(isPlacedAt Sofa_b5903624 Floor_9ce8d4dd)
		(isPlacedAt Desk_8c41b1c0 Floor_9ce8d4dd)
		(isPlacedAt Drawer_c1b1c71e Floor_9ce8d4dd)
		(isPlacedAt GarbageCan_92106b41 Floor_9ce8d4dd)
		(isPlacedAt Chair_a3bee7ce Floor_9ce8d4dd)
		(isPlacedAt Drawer_9950548b Floor_9ce8d4dd)
		(isPlacedAt SideTable_a9b9b711 Floor_9ce8d4dd)
		(isPlacedAt SideTable_b82ed100 Floor_9ce8d4dd)
		(isPlacedAt Drawer_03580458 Floor_9ce8d4dd)
		(atLocation Robot Floor_9ce8d4dd)
		(pickupable Pillow_974691ae)
		(temperature Pillow_974691ae RoomTemp)
		(isPlacedAt Pillow_974691ae Bed_b8ad3dcc)
		(temperature Bed_b8ad3dcc RoomTemp)
		(receptacle Bed_b8ad3dcc)
		(isPlacedAt Laptop_f57c484a Bed_b8ad3dcc)
		(isPlacedAt TeddyBear_cde4a75b Bed_b8ad3dcc)
		(isPlacedAt Bed_b8ad3dcc Floor_9ce8d4dd)
		(dirtyable Bed_b8ad3dcc)
		(isDirty Bed_b8ad3dcc)
	)
	(:goal (and
    (isPlacedAt Pillow_0c062a19 Bed_b8ad3dcc)
    (isPlacedAt Pillow_974691ae Bed_b8ad3dcc)
))
)