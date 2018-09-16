// rooms will be assigned a binary string that is 6 digits long indicating which of its
// six potential doors are realized; a room asisgned 000000 will have no doors (which is not possible)
// and a room assigned 111111 will have all doors (which should only be the case for the starting room)

// numbers represent doors starting from top left in clockwise order

// boss rooms (the rooms in the middle of the walls, e.g. (0, 2), (2, 0)) will always only have two doors open; 
// the ones joining them to the adjacent rooms that are not on the wall. so, room (2, 0) will have value
// 000110 and room (2, 0) will have value 001100. 

// method to generate: work from inside out? or, maybe both ways? have list of ones already created
// (middle and bosses), then do all ones connecting to that, then all connected to those, etc?

// need to ensure that all rooms can be reached; is it better to ensure that during generation,
// or just check afterward and then regenerate?

global.world_map = ds_grid_create(9, 17); // door connections
global.world_rooms = ds_grid_create(9, 17); // rooms visited
global.world_treasures = ds_grid_create(9, 17); // rewards in rooms
global.world_room_pattern = ds_grid_create(9, 17); // room layouts
global.deaths = ds_list_create(); // locations/times of deaths
global.rooms_over_time = ds_list_create(); // player route
global.time = "";

var floor_number = argument0; // use this for difficulty, treasure rarity, etc. later

generateWorldRoute();

global.current_coords = [4, 8];

// general todo:
// switch rooms
// clock
// draw map
// deaths
// keep track of route
// enemies, treasures, bosses, etc (generic stuff)

// ui can be put into the corners outside of the room! map top right, health/clock top left... items bottom left?