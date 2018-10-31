var startingRoomX = argument0;
var startingRoomY = argument1;

// determine which rooms you can get to from current room.
// on a valid map, when this function is run on the starting room
// it should include all the boss rooms.

var traversable_rooms = ds_list_create();
var starting_room = [startingRoomX, startingRoomY];
ds_list_add(traversable_rooms, starting_room);

for (var i=0; i < ds_list_size(traversable_rooms); i++) {
	var current_room = ds_list_find_value(traversable_rooms, i);
	var current_room_doors = ds_grid_get(global.world_map, current_room[0], current_room[1]);
	for (var j=1; j <= 6; j++) {
		if (string_char_at(current_room_doors, j) == "1") {
			var rel_pos = numToRelPos(j-1);
			var adjacent_room = getRelativeTile(current_room[0], current_room[1], rel_pos);
			show_debug_message(adjacent_room);
			show_debug_message(rel_pos);
			if (!checkArrayInDsList(traversable_rooms, adjacent_room)) {
				ds_list_add(traversable_rooms, adjacent_room);
			}
		}
	}
}

return traversable_rooms;