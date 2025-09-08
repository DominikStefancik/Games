import { MAP_SPRITE, ROOM_DATA_LAYER_NAME } from "../constants";
import { createPlayer } from "../entities/player";
import kaplayContext from "../kaplay-context";
import {
  setBackground,
  setCameraHorizontalControls,
  setCameraVerticalZones,
  setMapColliders,
} from "./helpers";
import type { RoomData } from "./models";

export const room1 = (roomData: RoomData) => {
  setBackground("#a2aed5");

  kaplayContext.setCamScale(4);
  kaplayContext.setCamPos(170, 100);
  kaplayContext.setGravity(1000);

  // method "add()" from Kaplay creates a game object and makes it visible in a scene
  // whereas the method "make()" from Kaplay just creates a game object, but doesn't make it visible
  //
  // the "map" game object will be a parent of everything and then its child game objects will be positioned
  // relatively to the "map" object
  const map = kaplayContext.add([
    kaplayContext.sprite(MAP_SPRITE.room1),
    kaplayContext.pos(),
  ]);

  const colliders = [];
  const positions = [];
  const cameras = [];

  for (const layer of roomData.layers) {
    switch (layer.name) {
      case ROOM_DATA_LAYER_NAME.colliders:
        colliders.push(...layer.objects);
        break;
      case ROOM_DATA_LAYER_NAME.positions:
        positions.push(...layer.objects);
        break;
      case ROOM_DATA_LAYER_NAME.cameras:
        cameras.push(...layer.objects);
        break;
      default:
        break;
    }
  }

  setMapColliders(map, colliders);
  setCameraVerticalZones(map, cameras);

  const playerPosition = positions.find(
    (position) => position.name === "player",
  )!;

  const player = map.add(createPlayer());
  player.setPosition(playerPosition.x, playerPosition.y);
  player.setControls();
  player.setEvents();
  player.enablePassthrough();

  setCameraHorizontalControls({ map, player, roomData });
};
