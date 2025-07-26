import {
  CONFIRM_UI_SOUND,
  CONTROLS_SCENE,
  ENTER_KEY,
  FOREST_BACKGROUND_SPRITE,
  LOGO_SPRITE,
} from "../constants";
import kaplayContext from "../kaplay-context";
import { displayBlinkingMessage } from "./helpers";

export const menu = () => {
  kaplayContext.add([
    kaplayContext.sprite(FOREST_BACKGROUND_SPRITE),
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
    kaplayContext.play(CONFIRM_UI_SOUND, { speed: 1.5 });
    kaplayContext.go(CONTROLS_SCENE);
  });
};
