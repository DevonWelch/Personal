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
global.world_indexes = ds_grid_create(9, 17); // indexes of rooms
global.deaths = ds_list_create(); // locations/times of deaths
//global.rooms_over_time = ds_list_create(); // player route
global.alive_bosses = ds_list_create();
global.dead_bosses = ds_list_create();

global.current_run = 1;

global.day_1_rooms = ds_list_create();
global.day_2_rooms = ds_list_create();
global.day_3_rooms = ds_list_create();
global.day_4_rooms = ds_list_create();
global.day_5_rooms = ds_list_create();
global.day_6_rooms = ds_list_create();

ds_grid_clear(global.world_indexes, -1);
ds_grid_set(global.world_indexes, 4, 8, room);

ds_list_add(global.day_1_rooms, [0, room]);

ds_list_add(global.alive_bosses, [4, 0]);
ds_list_add(global.alive_bosses, [8, 4]);
ds_list_add(global.alive_bosses, [8, 12]);
ds_list_add(global.alive_bosses, [4, 16]);
ds_list_add(global.alive_bosses, [0, 12]);
ds_list_add(global.alive_bosses, [0, 4]);

var floor_number = argument0; // use this for difficulty, treasure rarity, etc. later

global.current_coords = [4, 8];

generateWorldRoute();

// general todo:
// switch rooms
// clock
// draw map
// deaths
// keep track of route
// enemies, treasures, bosses, etc (generic stuff)


// have different boos layouts on different floors?
// ui can be put into the corners outside of the room! map top right, health/clock top left... items bottom left?