var room_1 = argument0;
var room_2 = argument1;

// returns -1 if not adjacent, otherwise number from 1-6 for string position of door for room1

var pos_list = ["tt", "ur", "lr", "tb", "ll", "ul"];

for (var i=0; i < array_length_1d(pos_list); i++) {
	if (array_equals(getRelativeTile(room_1[0], room_1[1], pos_list[i]), room_2)) {
		return i;
	}
}
return -1;