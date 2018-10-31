// argument0 = x_coord coordinate
// argument1 = y_coord coordinate
// argument2 = relative position: ul, ur, ll, lr (upper/lower left/right), tl, tr (true left/right)

var x_coord = argument0;
var y_coord = argument1;
var relPos = argument2;

// upper right: 
var ur = ((y_coord == 0) || (x_coord == 5 && y_coord == 1) ||
	(x_coord == 6 && y_coord == 2) || (x_coord == 7 && y_coord == 3) ||
	(x_coord == 8 && y_coord == 4));

// true right:
var tr = (x_coord == 8);

// lower right:
var lr = ((x_coord == 8 && y_coord == 12) || (x_coord == 7 && y_coord == 13) || 
(x_coord == 6 && y_coord == 14) || (x_coord == 5 && y_coord == 15) || y_coord == 16);

// lower left
var ll = (y_coord == 16 || (x_coord == 3 && y_coord == 15) || 
	   (x_coord == 2 && y_coord == 14) || (x_coord == 1 && y_coord == 13) ||
	   (x_coord == 0 && y_coord == 12));

// true left
var tl = (x_coord == 0);

// upper left
var ul = ((x_coord == 0 && y_coord == 4) || (x_coord == 1 && y_coord == 3) ||
		(x_coord == 2 && y_coord == 2) || (x_coord == 3 && y_coord == 1) ||
		y_coord == 0);

if (relPos == "tt") {
	if (ul || ur) {
		return []; // there is no such tile
	} else {
		return [x_coord, y_coord-2];	
	}
} else if (relPos == "ur") {
	if (ur || tr) {
		return []; // there is no such tile
	} else {
		return [x_coord+1, y_coord-1];	
	}
} else if (relPos == "lr") {
	if (tr || lr) {
		return []; // there is no such tile
	} else {
		return [x_coord+1, y_coord+1];	
	}
} else if (relPos == "tb") {
	if (lr || ll) {
		return []; // there is no such tile
	} else {
		return [x_coord, y_coord+2];	
	}
} else if (relPos == "ll") {
	if (ll || tl) {
		return []; // there is no such tile
	} else {
		return [x_coord-1, y_coord+1];
	}
} else if (relPos == "ul") {
	if (tl || ul) {
		return []; // there is no such tile
	} else {
		return [x_coord-1, y_coord-1];
	}
}