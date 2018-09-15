var my_ds_list = argument0
var my_array = argument1;

for (var i=0; i<ds_list_size(my_ds_list); i++) {
	if (array_equals(my_array, ds_list_find_value(my_ds_list, i))) {
		return true;
	}
}

return false;