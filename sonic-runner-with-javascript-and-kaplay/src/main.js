import { loadAssets } from "./assets-helpers";
import {
  GAME_OVER_SCENE_ID,
  GAME_SCENE_ID,
  MAIN_MENU_SCENE_ID,
} from "./constants";
import kaplayContext from "./kaplay-context";
import game from "./scenes/game";
import mainMenu from "./scenes/main-menu";

// first, load assets to the game
loadAssets();

// defines a scene shown in the game
kaplayContext.scene(MAIN_MENU_SCENE_ID, mainMenu);

kaplayContext.scene(GAME_SCENE_ID, game);

kaplayContext.scene(GAME_OVER_SCENE_ID, () => {});

// "go" defines which scene we should go to
kaplayContext.go(MAIN_MENU_SCENE_ID);
