import { MAP_SPRITE } from "../constants";
import { createPlayer } from "../entities/player";
import kaplayContext from "../kaplay-context";
import { setBackground, setMapColliders } from "./helpers";
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
  const map = kaplayContext.add([kaplayContext.sprite(MAP_SPRITE.room1)]);
  const colliders = roomData.layers.find(
    (layer) => layer.name == "colliders",
  )!.objects;
  setMapColliders(map, colliders);

  const positions = roomData.layers.find(
    (layer) => layer.name == "positions",
  )!.objects;
  const playerPosition = positions.find(
    (position) => position.name === "player",
  )!;

  const player = map.add(createPlayer());
  player.setPosition(playerPosition.x, playerPosition.y);
  player.setControls();
  player.setEvents();
  player.enablePassthrough();
};
