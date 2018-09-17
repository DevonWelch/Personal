/// @description Insert description here
// You can write your code in this editor

draw_text( 100, 100, string(global.hours) + ":" + string(global.minutes) + ":" + string(global.seconds) );

draw_text(100, 32, "FPS = " + string(fps));
draw_text(100, 52, "hspeed = " + string(hspeed));

var exploredRoomSprite = asset_get_index("exploredRoom");
var unexploredRoomSprite = asset_get_index("unexploredRoom");
var currentRoomSprite = asset_get_index("currentRoom");
var bossRoomSprite = asset_get_index("bossRoom");
var spriteWidth = sprite_get_width(currentRoomSprite);
var spriteHeight = sprite_get_height(currentRoomSprite);

// todo: add boss rooms
// add new room type for current room & bar room?

// should move all this to a function that runs on room chnage, and then aggregates it into one big sprite (somehow...)
// if can't do that... ds_list or something?
// looks like draw_surface is the function to use

for (var x_coord = 0; x_coord < 9; x_coord++) {
	for (var y_coord = 0; y_coord < 17; y_coord++) {
		var room_string = ds_grid_get(global.world_map, x_coord, y_coord);
		
		if (room_string != "uuuuuu") {
			var room_x_coord = 1635 + ((((4 * spriteWidth) + 2) * x_coord) / 5);
			var room_y_coord = 30 + ((spriteHeight / 2) + 2) * y_coord;
			var room_type = unexploredRoomSprite;
			if (x_coord == global.current_coords[0] && y_coord == global.current_coords[1]) {
				room_type = currentRoomSprite;
			} else if (checkArrayInDsList(global.alive_bosses, [x_coord, y_coord])) {
				room_type = bossRoomSprite;
			} else if (ds_grid_get(global.world_rooms, x_coord, y_coord) == 1) {
				room_type = exploredRoomSprite;
			}
			draw_sprite(room_type, 0, room_x_coord, room_y_coord);
		}
	}	
}

for (var x_coord = 0; x_coord < 9; x_coord++) {
	for (var y_coord = 0; y_coord < 17; y_coord++) {
		var room_string = ds_grid_get(global.world_map, x_coord, y_coord);
		
		if (room_string != "uuuuuu") {
			var room_x_coord = 1635 + ((((4 * spriteWidth) + 2) * x_coord) / 5);
			var room_y_coord = 30 + ((spriteHeight / 2) + 2) * y_coord;

			if (ds_grid_get(global.world_rooms, x_coord, y_coord) == 1 || checkArrayInDsList(global.alive_bosses, [x_coord, y_coord])) {
				for (var i = 1; i < 7; i++) {
					if (string_char_at(room_string, i) == "1") {
						var x1;
						var x2;
						var y1;
						var y2;
						
						if (i == 1) {
							x1 = room_x_coord - 26;
							x2 = room_x_coord - 26;
							y1 = room_y_coord - 15;
							y2 = room_y_coord - 28;
						} else if (i == 2) {
							x1 = room_x_coord - 15;
							x2 = room_x_coord - 5;
							y1 = room_y_coord - 13;
							y2 = room_y_coord - 20;
						} else if (i == 3) {
							x1 = room_x_coord - 15;
							x2 = room_x_coord - 5;
							y1 = room_y_coord - 4;
							y2 = room_y_coord + 3;
						} else if (i == 4) {
							x1 = room_x_coord - 26;
							x2 = room_x_coord - 26;
							y1 = room_y_coord - 1;
							y2 = room_y_coord + 12;
						} else if (i == 5) {
							x1 = room_x_coord - 40;
							x2 = room_x_coord - 50;
							y1 = room_y_coord - 4;
							y2 = room_y_coord + 3;
						} else if (i == 6) {
							x1 = room_x_coord - 40;
							x2 = room_x_coord - 50;
							y1 = room_y_coord - 13;
							y2 = room_y_coord - 20;
						}
						
						draw_line_width_color(x1, y1, x2, y2, 3, c_white, c_white);
					}
				}
			}
		}
	}	
}

