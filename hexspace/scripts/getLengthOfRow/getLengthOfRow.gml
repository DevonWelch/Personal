// argument0 is the y_coord value of the row

var y_coord = argument0;

if (y_coord == 0 || y_coord == 16) {
	return 1;
} else if (y_coord == 1 || y_coord == 15) {
	return 2;
} else if (y_coord == 2 || y_coord == 14) {
	return 3;
} else if (y_coord == 3 || y_coord == 5 || y_coord == 7 || y_coord == 9 || y_coord == 11 || y_coord == 13) {
	return 4;
} else if (y_coord == 4 || y_coord == 6 || y_coord == 8 || y_coord == 10 || y_coord == 12) {
	return 5;
}