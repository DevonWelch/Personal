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

