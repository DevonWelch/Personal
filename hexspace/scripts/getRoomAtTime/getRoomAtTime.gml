var run = argument0;
var time_to_get = argument1;

var run_rooms = getRoomsForRun(run);

for (var i=1; i < ds_list_size(run_rooms); i++) {
	var time_and_room = ds_list_find_value(run_rooms, i);
	if (time_and_room[0] > time_to_get) {
		var time_and_room_2 = ds_list_find_value(run_rooms, i - 1);
		return time_and_room_2[1];
	}
}
// didn't find it so must be last one
var time_and_room = ds_list_find_value(run_rooms, ds_list_size(run_rooms) - 1);
return time_and_room[1];