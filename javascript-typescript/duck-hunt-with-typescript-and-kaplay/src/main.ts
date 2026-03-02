import { SCENE } from "./constants";
import { loadEntitiesAssets } from "./entities/assets-loader";
import kaplayContext from "./kaplay-context";
import { loadSceneAssets } from "./scenes/assets-loader";
import { game } from "./scenes/game";
import gameOver from "./scenes/game-over";
import { mainMenu } from "./scenes/main-menu";

loadSceneAssets();
loadEntitiesAssets();

kaplayContext.scene(SCENE.mainMenu, mainMenu);

kaplayContext.scene(SCENE.game, game);

kaplayContext.scene(SCENE.gameOver, gameOver);

kaplayContext.go(SCENE.mainMenu);
