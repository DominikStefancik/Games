import {
  GAME_OVER_SCENE_ID,
  GAME_SCENE_ID,
  MAIN_MENU_SCENE_ID,
} from "./constants";
import kaplayContext from "./kaplay-context";
import { loadSceneAssets } from "./scenes/assets-loader";
import { mainMenu } from "./scenes/main-menu";

loadSceneAssets();

kaplayContext.scene(MAIN_MENU_SCENE_ID, mainMenu);

kaplayContext.scene(GAME_SCENE_ID, () => {});

kaplayContext.scene(GAME_OVER_SCENE_ID, () => {});

kaplayContext.go(MAIN_MENU_SCENE_ID);
