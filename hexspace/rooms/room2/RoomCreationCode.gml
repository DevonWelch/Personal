var roomBackgroundSprite = asset_get_index("roomBackground");
var background_layer = layer_create(2000);
var background_layer_2 = layer_background_create(background_layer, roomBackgroundSprite);
displayDoors(room);