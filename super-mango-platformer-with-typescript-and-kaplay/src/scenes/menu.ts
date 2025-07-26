import type { GameObj, Vec2 } from "kaplay";
import {
  CONFIRM_UI_SOUND,
  CONTROLS_SCENE,
  ENTER_KEY,
  FOREST_BACKGROUND_SPRITE,
  LOGO_SPRITE,
  ROUND_FONT,
  TEXT_FLASH_DOWN_STATE,
  TEXT_FLASH_UP_STATE,
} from "../constants";
import kaplayContext from "../kaplay-context";

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

const displayBlinkingMessage = (text: string, position: Vec2): GameObj => {
  const message = kaplayContext.add([
    kaplayContext.text(text, { size: 24, font: ROUND_FONT }),
    // we have to use the "area" component, because later we want to use the "anchor" component
    kaplayContext.area(),
    // the "anchor" component cannot be used without the "area" component
    kaplayContext.anchor("center"),
    kaplayContext.pos(position),
    kaplayContext.opacity(),
    // a state machine for a blinking message
    kaplayContext.state(TEXT_FLASH_UP_STATE, [
      TEXT_FLASH_UP_STATE,
      TEXT_FLASH_DOWN_STATE,
    ]),
  ]);

  /*
   * A blinking effect is done by changing the message states, between "flash-up" and "flash-down"
   * When the "flash-up" state is entered, the text opacity is slowly (by tweening) decreased to 0
   * When the "flash-do" state is entered, the text opacity is slowly (by tweening) increased to 1
   * After each state finishes, the another is entered
   */
  message.onStateEnter(TEXT_FLASH_UP_STATE, async () => {
    await kaplayContext.tween(
      message.opacity,
      0,
      0.5,
      (newOpacity) => (message.opacity = newOpacity),
      kaplayContext.easings.linear,
    );

    message.enterState(TEXT_FLASH_DOWN_STATE);
  });

  message.onStateEnter(TEXT_FLASH_DOWN_STATE, async () => {
    await kaplayContext.tween(
      message.opacity,
      1,
      0.5,
      (newOpacity) => (message.opacity = newOpacity),
      kaplayContext.easings.linear,
    );

    message.enterState(TEXT_FLASH_UP_STATE);
  });

  return message;
};
