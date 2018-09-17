/// @description Insert description here
// You can write your code in this editor
if (vspeed > 0) {
	vspeed = vspeed - (delta_time / 1000000) * 20;
	if (vspeed < 0) {
		vspeed = 0;
	}
} else if (vspeed < 0) {
	vspeed = vspeed + (delta_time / 1000000) * 20;
	if (vspeed > 0) {
		vspeed = 0;
	}
}

if (hspeed > 0) {
	hspeed = hspeed - (delta_time / 1000000) * 20;
	if (hspeed < 0) {
		hspeed = 0;
	}
} else if (hspeed < 0) {
	hspeed = hspeed + (delta_time / 1000000) * 20;
	if (hspeed > 0) {
		hspeed = 0;
	}
}

global.my_time = global.my_time + delta_time;
if (global.my_time >= 86400000000) {
	global.my_time = 0;
} // 60 sec x 60 min x 24 hours = 86400 seconds in a day.
global.seconds = (global.my_time / 1000000) mod 60;
global.minutes = (global.my_time / 1000000) div 60 mod 60;
global.hours = (global.my_time / 1000000) div 3600;