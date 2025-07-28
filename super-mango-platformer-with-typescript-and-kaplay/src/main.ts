import { SCENE } from "./constants";
import kaplayContext from "./kaplay-context";
import { loadSceneAssets } from "./scenes/assets-loader";
import { controls } from "./scenes/controls";
import { level1 } from "./scenes/levels/level1";
import { menu } from "./scenes/menu";

loadSceneAssets();

const scenes: { [key: string]: () => void } = {
  [SCENE.menu]: menu,
  [SCENE.controls]: controls,
  [SCENE.firstLevel]: level1,
  [SCENE.secondLevel]: () => {},
  [SCENE.thirdLevel]: () => {},
  [SCENE.gameFinished]: () => {},
  [SCENE.gameOver]: () => {},
};

// create scenes
for (const gameScene of Object.keys(scenes)) {
  kaplayContext.scene(gameScene, scenes[gameScene]);
}

// specify a default scene which will be loaded when the game starts
kaplayContext.go(SCENE.menu);
