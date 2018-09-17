/// @description Insert description here
// You can write your code in this editor
if (vspeed > 0) {
	if (vspeed == 1) {
		vspeed = 0;
	} else {
		vspeed = vspeed - 2;
	}
} else if (vspeed < 0) {
	if (vspeed == -1) {
		vspeed = 0;
	} else {
		vspeed = vspeed + 2;
	}
}

if (hspeed > 0) {
	if (hspeed == 1) {
		hspeed = 0;
	} else {
		hspeed = hspeed - 2;
	}
} else if (hspeed < 0) {
	if (hspeed == -1) {
		hspeed = 0;
	} else {
		hspeed = hspeed + 2;
	}
}

global.my_time = global.my_time + delta_time;
if (global.my_time >= 86400000000) {
	global.my_time = 0;
} // 60 sec x 60 min x 24 hours = 86400 seconds in a day.
global.seconds = (global.my_time / 1000000) mod 60;
global.minutes = (global.my_time / 1000000) div 60 mod 60;
global.hours = (global.my_time / 1000000) div 3600;