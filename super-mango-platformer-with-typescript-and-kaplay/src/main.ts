import {
  CONTROLS_SCENE,
  FIRST_LEVEL_SCENE,
  GAME_FINISHED_SCENE,
  GAME_OVER_SCENE,
  MENU_SCENE,
  SECOND_LEVEL_SCENE,
  THIRD_LEVEL_SCENE,
} from "./constants";
import kaplayContext from "./kaplay-context";
import { loadSceneAssets } from "./scenes/assets-loader";
import { menu } from "./scenes/menu";

loadSceneAssets();

const scenes: { [key: string]: () => void } = {
  [MENU_SCENE]: menu,
  [CONTROLS_SCENE]: () => {},
  [FIRST_LEVEL_SCENE]: () => {},
  [SECOND_LEVEL_SCENE]: () => {},
  [THIRD_LEVEL_SCENE]: () => {},
  [GAME_FINISHED_SCENE]: () => {},
  [GAME_OVER_SCENE]: () => {},
};

// create scenes
for (const gameScene of Object.keys(scenes)) {
  kaplayContext.scene(gameScene, scenes[gameScene]);
}

// specify a default scene which will be loaded when the game starts
kaplayContext.go(MENU_SCENE);
