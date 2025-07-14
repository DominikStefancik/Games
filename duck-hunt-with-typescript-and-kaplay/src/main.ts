import {
  GAME_OVER_SCENE_ID,
  GAME_SCENE_ID,
  MAIN_MENU_SCENE_ID,
} from "./constants";
import kaplayContext from "./kaplay-context";

//
kaplayContext.scene(MAIN_MENU_SCENE_ID, () => {});

kaplayContext.scene(GAME_SCENE_ID, () => {});

kaplayContext.scene(GAME_OVER_SCENE_ID, () => {});

kaplayContext.go(MAIN_MENU_SCENE_ID);
