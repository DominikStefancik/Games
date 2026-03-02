import { SCENE } from "./constants";
import kaplayContext from "./kaplay-context";
import { loadSceneAssets } from "./assets-loader";
import { controls } from "./scenes/controls";
import { level1 } from "./scenes/levels/level1";
import { level2 } from "./scenes/levels/level2";
import { level3 } from "./scenes/levels/level3";
import { menu } from "./scenes/menu";
import { gameOver } from "./scenes/game-over";
import { gameFinished } from "./scenes/game-finished";

loadSceneAssets();

const scenes: { [key: string]: () => void } = {
  [SCENE.menu]: menu,
  [SCENE.controls]: controls,
  [SCENE.level1]: level1,
  [SCENE.level2]: level2,
  [SCENE.level3]: level3,
  [SCENE.gameFinished]: gameFinished,
  [SCENE.gameOver]: gameOver,
};

// create scenes
for (const gameScene of Object.keys(scenes)) {
  kaplayContext.scene(gameScene, scenes[gameScene]);
}

// specify a default scene which will be loaded when the game starts
kaplayContext.go(SCENE.menu);
