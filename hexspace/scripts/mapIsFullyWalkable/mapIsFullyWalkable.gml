// no arguments, just world map?

var walking_map = ds_grid_create(9, 9); // use this to keep track of explored tiles

// start from center and then pursue every open path and add every new tile to list of tiles to 
// explore from; remove explored tiles from list and set them as explored in walking_map.
// repeat process but don't add explored tiles to list

// don't need to do that, can just check that all rooms have at least one... in which case, it should also be relativel simple to fix, 
// just add a one. has ot be slightly sophisticated though, probably make sure that the room being connected to already
// had at least one one, and that it's not a boss room