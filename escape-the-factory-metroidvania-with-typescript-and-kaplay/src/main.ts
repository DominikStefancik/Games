import { SCENE } from "./constants";
import kaplayContext from "./kaplay-context";
import { intro } from "./scenes/intro";
import { room1 } from "./scenes/room1";
import { room2 } from "./scenes/room2";

const scenes: { [key: string]: () => void } = {
  [SCENE.intro]: intro,
  [SCENE.room1]: () => {
    room1();
  },
  [SCENE.room2]: () => {
    room2();
  },
};

// create scenes
for (const gameScene of Object.keys(scenes)) {
  kaplayContext.scene(gameScene, scenes[gameScene]);
}

// specify a default scene which will be loaded when the game starts
kaplayContext.go(SCENE.intro);
