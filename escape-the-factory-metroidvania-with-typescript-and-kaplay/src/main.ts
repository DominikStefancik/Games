import { loadSceneAssets } from "./assets-loader";
import { SCENE } from "./constants";
import kaplayContext from "./kaplay-context";
import { intro } from "./scenes/intro";
import type { RoomData, SceneData } from "./scenes/models";
import { room1 } from "./scenes/room1";
import { room2 } from "./scenes/room2";

loadSceneAssets();

const scenes: { [key: string]: (previousSceneData: SceneData) => void } = {
  [SCENE.intro]: intro,
  [SCENE.room1]: async (previousSceneData: SceneData) => {
    const room1Data = (await kaplayContext.loadJSON(
      "room1Data",
      "./maps/room1.json",
    )) as RoomData;
    room1(room1Data, previousSceneData);
  },
  [SCENE.room2]: async (previousSceneData: SceneData) => {
    const room2Data = (await kaplayContext.loadJSON(
      "room2Data",
      "./maps/room2.json",
    )) as RoomData;
    room2(room2Data, previousSceneData);
  },
};

// create scenes
for (const gameScene of Object.keys(scenes)) {
  kaplayContext.scene(gameScene, scenes[gameScene]);
}

// specify a default scene which will be loaded when the game starts
kaplayContext.go(SCENE.intro);
