import {
  BACKGROUND_SPRITE,
  ENTER_KEY,
  LOGO_SPRITE,
  SCENE,
  SOUND,
} from "../constants";
import kaplayContext from "../kaplay-context";
import { displayBlinkingMessage } from "./helpers";

export const menu = () => {
  kaplayContext.add([
    kaplayContext.sprite(BACKGROUND_SPRITE.forest),
    kaplayContext.scale(4),
  ]);
  kaplayContext.add([
    kaplayContext.sprite(LOGO_SPRITE),
    kaplayContext.scale(8),
    // we have to use the "area" component, because later we want to use the "anchor" component
    kaplayContext.area(),
    // the "anchor" component cannot be used without the "area" component
    kaplayContext.anchor("center"),
    kaplayContext.pos(kaplayContext.center().x, kaplayContext.center().y - 200),
  ]);

  displayBlinkingMessage(
    "Press [ Enter ] to start the game",
    kaplayContext.vec2(
      kaplayContext.center().x,
      kaplayContext.center().y + 100,
    ),
  );

  kaplayContext.onKeyPress(ENTER_KEY, () => {
    kaplayContext.play(SOUND.confirmUi, { speed: 1.5 });
    kaplayContext.go(SCENE.controls);
  });
};
