var routeValid = false;

var startingRoomRoute = findTraversableRooms(global.current_coords[0], global.current_coords[1]);

for (var i=0; i<ds_list_size(global.alive_bosses); i++) {
	if (!checkArrayInDsList(startingRoomRoute, ds_list_find_value(global.alive_bosses, i))) {
		var boss_room = ds_list_find_value(global.alive_bosses, i);
		show_debug_message("boss room:");
		show_debug_message(boss_room);
		var bossRoute = findTraversableRooms(boss_room[0], boss_room[1]);
		addConnectingDoor(startingRoomRoute, bossRoute);
		startingRoomRoute = findTraversableRooms(global.current_coords[0], global.current_coords[1]);
	}
}