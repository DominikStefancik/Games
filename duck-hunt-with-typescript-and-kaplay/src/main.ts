import {
  GAME_OVER_SCENE_ID,
  GAME_SCENE_ID,
  MAIN_MENU_SCENE_ID,
} from "./constants";
import { loadEntitiesAssets } from "./entities/assets-loader";
import kaplayContext from "./kaplay-context";
import { loadSceneAssets } from "./scenes/assets-loader";
import { game } from "./scenes/game";
import gameOver from "./scenes/game-over";
import { mainMenu } from "./scenes/main-menu";

loadSceneAssets();
loadEntitiesAssets();

kaplayContext.scene(MAIN_MENU_SCENE_ID, mainMenu);

kaplayContext.scene(GAME_SCENE_ID, game);

kaplayContext.scene(GAME_OVER_SCENE_ID, gameOver);

kaplayContext.go(MAIN_MENU_SCENE_ID);
