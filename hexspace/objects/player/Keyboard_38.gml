/// @description Insert description here
// You can write your code in this editor
vspeed = min(vspeed - (delta_time / 1000000) * 30, -1);
if (vspeed < -5) {
	vspeed = -5;
}