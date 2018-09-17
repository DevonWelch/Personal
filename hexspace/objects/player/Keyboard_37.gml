/// @description Insert description here
// You can write your code in this editor
hspeed = min(hspeed - (delta_time / 1000000) * 30, -1);
if (hspeed < -5) {
	hspeed = -5;
}