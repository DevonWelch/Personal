var doorNum = argument0;

var relPos = numToRelPos(doorNum);

var newCoords = getRelativeTile(global.current_coords[0], global.current_coords[1], relPos);

global.current_coords = [newCoords[0], newCoords[1]];

var go_to_room;

if (ds_grid_get(global.world_indexes, newCoords[0], newCoords[1]) != -1) {
	go_to_room = ds_grid_get(global.world_indexes, newCoords[0], newCoords[1]);
} else {

	var default_room = asset_get_index("room2");

	//var new_room = room_add();
	var new_room = room_duplicate(default_room);
	room_set_width(new_room, 1920);
	room_set_height(new_room, 1080);

	ds_grid_set(global.world_indexes, newCoords[0], newCoords[1], new_room);
	ds_grid_set(global.world_rooms, newCoords[0], newCoords[1], 1);

	go_to_room = new_room;
	// fade to black, switch rooms?

	// should add to some global array of room changes over time
	// what's the best way to do that? keep a ds_list of player's position at every in-game minute?
	// seems inefficient... there would be 60*16*6 = 5760 total entries (hours*minutes*days), and it'd be a ds_list of arrays
	// one alternative might be just keep a list of times when room is changed. but problem is that then lookup
	// at a certain time is less efficient... but assuming ~30 rooms on one day, entries would be reduced to 180. 
	// and to find location at a time would have to do a loop of 15 on average. so, pretty good
	// should it be list, in format [time, room]? or maybe {time: room}? probably easier to loop through former
}
room_goto(go_to_room);
global.current_room = go_to_room;

if (global.current_run == 1) {
	ds_list_add(global.day_1_rooms, [global.my_time, go_to_room]);
} else if (global.current_run == 2) {
	ds_list_add(global.day_2_rooms, [global.my_time, go_to_room]);
} else if (global.current_run == 3) {
	ds_list_add(global.day_3_rooms, [global.my_time, go_to_room]);
} else if (global.current_run == 4) {
	ds_list_add(global.day_4_rooms, [global.my_time, go_to_room]);
} else if (global.current_run == 5) {
	ds_list_add(global.day_5_rooms, [global.my_time, go_to_room]);
} else if (global.current_run == 6) {
	ds_list_add(global.day_6_rooms, [global.my_time, go_to_room]);
}
// might want a map, {room: [[x, y]}
