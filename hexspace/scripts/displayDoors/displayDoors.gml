var current_room_doors = ds_grid_get(global.world_map, global.current_coords[0], global.current_coords[1]);

for (var i=1; i<=6; i++) {
	show_debug_message(i);
	var current_door = string_char_at(current_room_doors, i);
	show_debug_message(current_door);
	// display the door
	if (current_door == "1") {
		var x_coord;
		var y_coord;
		if (i == 1) {
			x_coord = 960;
			y_coord = 20;
		} else if (i == 2) {
			x_coord = 1536;
			y_coord = 270;
		} else if (i == 3) {
			x_coord = 1536;
			y_coord = 810;
		} else if (i == 4) {
			x_coord = 960;
			y_coord = 1060;
		} else if (i == 5) {
			x_coord = 384;
			y_coord = 810;
		} else if (i == 6) {
			x_coord = 384;
			y_coord = 270;
		}
		show_debug_message(x_coord);
		show_debug_message(y_coord);
		var inst = instance_create_depth(x_coord, y_coord, 10, doorObj);
		inst.door_num = i - 1;
		show_debug_message(inst.door_num);
	}
}
