// first, set ALL tiles to unknown ("uuuuuu")
randomize();

ds_grid_clear(global.world_map, "uuuuuu");
ds_grid_clear(global.world_rooms, 0);
ds_grid_set(global.world_rooms, 4, 8, 1);
// important note: while reading ds_grid in debug info, the first, value is x and the second is y.
// this goes against intuition of what it looks like re: cols and rows.

// first index of string is top, and then continues clockwise
// and, because teh grid is now stacked, it won't be 10 x 10...

ds_grid_set(global.world_map, 4, 8, "111111");
ds_grid_set(global.world_map, 4, 0, "000100");
ds_grid_set(global.world_map, 8, 4, "000010");
ds_grid_set(global.world_map, 8, 12, "000001");
ds_grid_set(global.world_map, 4, 16, "100000");
ds_grid_set(global.world_map, 0, 12, "010000");
ds_grid_set(global.world_map, 0, 4, "001000");

var seen_rooms = ds_list_create();
var reached_rooms = ds_list_create();
var done_rooms = ds_list_create();

ds_list_add(reached_rooms, [4,8], [4,0], [8,4], [8,12], [4,16], [0,12], [0,4]);

// first, fill out any values that these would necessitate in other rooms, and add those rooms to seen_rooms.
// then, move these rooms to done rooms
// then, fill out remaining values in seen_rooms and move them to reached_rooms. repeat until no more rooms
// don't forget - 0s are as importans as 1s!

var room_string;
var next_seen_room_string;

while (!ds_list_empty(reached_rooms)) {
	for (var i=0; i < ds_list_size(reached_rooms); i++) {
		var coords = ds_list_find_value(reached_rooms, i);
		room_string = ds_grid_get(global.world_map, coords[0], coords[1]);
		
		for (j=0; j<6; j++) {
			// for each door/no door, find appropriate room and assign appropriate value
			
			var relPos = numToRelPos(j);
			var relRoomCoords = getRelativeTile(coords[0], coords[1], relPos);
			
			if (array_length_1d(relRoomCoords) != 0) {
				var relRoomString = ds_grid_get(global.world_map, relRoomCoords[0], relRoomCoords[1]);
				var relRoomDoor = getOppositeDoor(j);
				
				relRoomString = string_delete(relRoomString, relRoomDoor+1, 1);
				relRoomString = string_insert(string_char_at(room_string, j+1), relRoomString, relRoomDoor+1);
				
				ds_grid_set(global.world_map, relRoomCoords[0], relRoomCoords[1], relRoomString);
				
				if (!checkArrayInDsList(seen_rooms, relRoomCoords) &&
					!checkArrayInDsList(done_rooms, relRoomCoords) && 
					!checkArrayInDsList(reached_rooms, relRoomCoords)) {
					ds_list_add(seen_rooms, relRoomCoords);
				}
			}
		}
	}
		
	// move all reached to done
	for(var k=0;k<ds_list_size(reached_rooms);k++) {
		ds_list_add(done_rooms, ds_list_find_value(reached_rooms, k));
	}
	ds_list_clear(reached_rooms);
		
	// fill all unknowns in seen, ensuring no coflicts
	// one way to ensure no conflicts: if connecting room is currently in reached, 
	// set value in other room at same time?
	for (var l=0; l<ds_list_size(seen_rooms); l++) {
		var next_seen_room = ds_list_find_value(seen_rooms, l);
		next_seen_room_string = ds_grid_get(global.world_map, next_seen_room[0], next_seen_room[1]);
		var nsr_char;
			
		for (var m=0; m<6; m++) {
			nsr_char = string_char_at(next_seen_room_string, m+1);
				
			if (nsr_char == "u") {
				var connected_room = getRelativeTile(next_seen_room[0], next_seen_room[1], numToRelPos(m));
					
				var door_val;
				// check that connecting room is within bounds. don't do anything if it's not
				// (although maybe add secret rooms or something)
				if (array_length_1d(connected_room) == 0) {
					door_val = "0";
				} else {
					// randomly choose whether there'll be a door (2/5 chance?)
					var rand = random(5);
					if (rand >= 3) {
						door_val = "1";
					} else {
						door_val = "0";
					}
				}
				// add it
				next_seen_room_string = string_delete(next_seen_room_string, m+1, 1);
				next_seen_room_string = string_insert(door_val, next_seen_room_string, m+1);
				
				// check if connecting room is in seen rooms, if it is, set it there as well
				if (checkArrayInDsList(seen_rooms, connected_room) && array_length_1d(connected_room) != 0) {
					// modify neighbour's door
					var connected_room_string = ds_grid_get(global.world_map, connected_room[0], connected_room[1]);
					var door_pos = getOppositeDoor(m);
					
					connected_room_string = string_delete(connected_room_string, door_pos+1, 1);
					connected_room_string = string_insert(door, connected_room_string, door_pos+1);
					ds_grid_set(global.world_map, connected_room[0], connected_room[1], connected_room_string);
				}
			}
		}
		
		ds_grid_set(global.world_map, next_seen_room[0], next_seen_room[1], next_seen_room_string);
	}
		
	// move seen to reached
	for(var n=0;n<ds_list_size(seen_rooms);n++) {
		ds_list_add(reached_rooms, ds_list_find_value(seen_rooms, n));
	}
	ds_list_clear(seen_rooms);
}



// destroy all temporary ds_lists
ds_list_destroy(seen_rooms);
ds_list_destroy(reached_rooms);
ds_list_destroy(done_rooms);