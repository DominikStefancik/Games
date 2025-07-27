import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import { ROUND_FONT, TEXT_STATE } from "../constants";

export const displayBlinkingMessage = (
  text: string,
  position: Vec2,
): GameObj => {
  const message = kaplayContext.add([
    kaplayContext.text(text, { size: 24, font: ROUND_FONT }),
    // we have to use the "area" component, because later we want to use the "anchor" component
    kaplayContext.area(),
    // the "anchor" component cannot be used without the "area" component
    kaplayContext.anchor("center"),
    kaplayContext.pos(position),
    kaplayContext.opacity(),
    // a state machine for a blinking message
    kaplayContext.state(TEXT_STATE.flashUp, [
      TEXT_STATE.flashUp,
      TEXT_STATE.flashDown,
    ]),
  ]);

  /*
   * A blinking effect is done by changing the message states, between "flashUp" and "flashDown"
   * When the "flashUp" state is entered, the text opacity is slowly (by tweening) decreased to 0
   * When the "flashDown" state is entered, the text opacity is slowly (by tweening) increased to 1
   * After each state finishes, the another is entered
   */
  message.onStateEnter(TEXT_STATE.flashUp, async () => {
    await kaplayContext.tween(
      message.opacity,
      0,
      0.5,
      (newOpacity) => (message.opacity = newOpacity),
      kaplayContext.easings.linear,
    );

    message.enterState(TEXT_STATE.flashDown);
  });

  message.onStateEnter(TEXT_STATE.flashDown, async () => {
    await kaplayContext.tween(
      message.opacity,
      1,
      0.5,
      (newOpacity) => (message.opacity = newOpacity),
      kaplayContext.easings.linear,
    );

    message.enterState(TEXT_STATE.flashUp);
  });

  return message;
};
