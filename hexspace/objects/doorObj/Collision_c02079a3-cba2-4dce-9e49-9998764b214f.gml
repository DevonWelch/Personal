/// @description Insert description here
// You can write your code in this editor
changeRoom(door_num);

show_debug_message("other:");
show_debug_message(other);
show_debug_message(other.x);

other.hspeed = 0;
other.vspeed = 0;

// might want to use getOppositeDoor,
// and then have some global dict of door positions...
//if (door_num == 0) {
//	other.x = 
//}
other.x = 960;
other.y = 540;