import kaplayContext from "../kaplay-context";
import { COLOR, FONT_CONFIG, SCENE } from "../constants";

const gameOver = () => {
  kaplayContext.add([
    kaplayContext.rect(kaplayContext.width(), kaplayContext.height()),
    kaplayContext.color(COLOR.BLACK),
  ]);
  kaplayContext.add([
    kaplayContext.text("GAME OVER!", FONT_CONFIG),
    kaplayContext.anchor("center"),
    kaplayContext.pos(kaplayContext.center()),
  ]);

  kaplayContext.wait(2, () => {
    kaplayContext.go(SCENE.mainMenu);
  });
};

export default gameOver;
