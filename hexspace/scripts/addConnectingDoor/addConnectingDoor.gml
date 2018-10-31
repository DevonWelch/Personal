var room_list_1 = argument0;
var room_list_2 = argument1;

for (var i=0; i < ds_list_size(room_list_1); i++) {
	var room_1 = ds_list_find_value(room_list_1, i);
	if (checkArrayInDsList(global.alive_bosses, room_1)) {
		continue;
	}
	for (var j=0; j < ds_list_size(room_list_2); j++) {
		var room_2 = ds_list_find_value(room_list_2, j);
		if (checkArrayInDsList(global.alive_bosses, room_2)) {
			continue;
		}
		
		var adjacency = getAdjacency(room_1, room_2);
		if (adjacency > -1) {
			// add connecting door
			var room_1_str = ds_grid_get(global.world_map, room_1[0], room_1[1]);
			room_1_str = string_delete(room_1_str, adjacency+1, 1);
			room_1_str = string_insert(1, room_1_str, adjacency+1);
			ds_grid_set(global.world_map, room_1[0], room_1[1], room_1_str);
			
			var opposite_door = getOppositeDoor(adjacency);
			var room_2_str = ds_grid_get(global.world_map, room_2[0], room_2[1]);
			room_2_str = string_delete(room_2_str, opposite_door+1, 1);
			room_2_str = string_insert(1, room_2_str, opposite_door+1);
			ds_grid_set(global.world_map, room_2[0], room_2[1], room_2_str);
						
			i = ds_list_size(room_list_1);
			j = ds_list_size(room_list_2);
		}
	}
}

// loop through first
// loop through second
// make sure neither room is boss room
// determine if door form first is adjacent to second
// if it is, add door
// then return