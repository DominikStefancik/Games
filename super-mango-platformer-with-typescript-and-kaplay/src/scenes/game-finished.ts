import { KEY_CONTROL, ROUND_FONT, SCENE, SCREEN, SOUND } from "../constants";
import kaplayContext from "../kaplay-context";
import { displayBlinkingMessage } from "./utils/helpers";

export const gameFinished = () => {
  kaplayContext.add([
    kaplayContext.rect(SCREEN.width, SCREEN.height),
    kaplayContext.color(0, 0, 0),
  ]);
  kaplayContext.add([
    kaplayContext.text("You won! Thanks for playing", {
      size: 50,
      font: ROUND_FONT,
    }),
    kaplayContext.area(),
    kaplayContext.anchor("center"),
    kaplayContext.pos(kaplayContext.center()),
  ]);

  displayBlinkingMessage(
    "Press [ Enter ] to play again",
    kaplayContext.vec2(
      kaplayContext.center().x,
      kaplayContext.center().y + 100,
    ),
  );

  kaplayContext.onKeyPress(KEY_CONTROL.enter, () => {
    kaplayContext.play(SOUND.confirmUi, { speed: 1.5 });
    kaplayContext.go(SCENE.menu);
  });
};
