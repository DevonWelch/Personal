/// @description Insert description here
// You can write your code in this editor

draw_text( 100, 100, string(global.hours) + ":" + string(global.minutes) + ":" + string(global.seconds) );

var miniRoomSprite = asset_get_index("miniRoom");
var spriteWidth = sprite_get_width(miniRoomSprite);
var spriteHeight = sprite_get_height(miniRoomSprite);

// can probably loop through them using 0-9, 0-9
// then check stuff using grids

for (var x_coord = 0; x_coord < 9; x_coord++) {
	for (var y_coord = 0; y_coord < 17; y_coord++) {
		var room_string = ds_grid_get(global.world_map, x_coord, y_coord);
		
		if (room_string != "uuuuuu") {
			var room_x_coord = 1475 + ((((4 * spriteWidth) + 2) * x_coord) / 5);
			var room_y_coord = 30 + ((spriteHeight / 2) + 2) * y_coord;
			draw_sprite(miniRoomSprite, 0, room_x_coord, room_y_coord);
		}
		
		if (ds_grid_get(global.world_map, x_coord, y_coord) == 1) {
			for (var i = 1; i < 7; i++) {
				// todo: draw conections
			}
		}
	}	
}

//draw_sprite(miniRoomSprite, 0, 1800, 20);
//var spriteWidth = sprite_get_width(miniRoomSprite);
//var spriteHeight = sprite_get_height(miniRoomSprite);
//draw_sprite(miniRoomSprite, 0, 1800 - (4 * spriteWidth / 5), 20 + (spriteHeight / 2) + 2);
//draw_sprite(miniRoomSprite, 0, 1800 + (4 * spriteWidth / 5), 20 + (spriteHeight / 2) + 2);
//draw_sprite(miniRoomSprite, 0, 1800, 20 + spriteHeight + 4);