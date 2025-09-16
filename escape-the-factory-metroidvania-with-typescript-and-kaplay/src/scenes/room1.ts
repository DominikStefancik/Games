import {
  MAP_SPRITE,
  ROOM_BACKGROUND_COLOR,
  SCENE,
  VERTICAL_BOUND,
} from "../constants";
import { setUpRoomMap } from "../helpers";
import kaplayContext from "../kaplay-context";
import { setBackground } from "./helpers";
import type { RoomData, SceneData } from "./models";

export const room1 = (roomData: RoomData, previousSceneData: SceneData) => {
  setBackground(ROOM_BACKGROUND_COLOR);

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

  setUpRoomMap({
    map,
    roomData,
    scene: SCENE.room1,
    verticalBound: VERTICAL_BOUND.room1,
    previousSceneData,
  });
};
