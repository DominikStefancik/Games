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

export const room2 = (roomData: RoomData, previousSceneData: SceneData) => {
  setBackground(ROOM_BACKGROUND_COLOR);

  kaplayContext.setCamScale(4);
  kaplayContext.setCamPos(170, 100);
  kaplayContext.setGravity(1000);

  // the "map" game object will be a parent of everything and then its child game objects will be positioned
  // relatively to the "map" object
  const map = kaplayContext.add([
    kaplayContext.sprite(MAP_SPRITE.room2),
    kaplayContext.pos(),
  ]);

  setUpRoomMap({
    map,
    roomData,
    scene: SCENE.room2,
    verticalBound: VERTICAL_BOUND.room2,
    previousSceneData,
  });
};
