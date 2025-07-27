import {
  BACKGROUND_SPRITE,
  KEY_CONTROL_SPRITE,
  ENTER_KEY,
  ROUND_FONT,
  SCENE,
  SOUND,
} from "../constants";
import kaplayContext from "../kaplay-context";
import { displayBlinkingMessage } from "./helpers";

export const controls = () => {
  kaplayContext.add([
    kaplayContext.sprite(BACKGROUND_SPRITE.forest),
    kaplayContext.scale(4),
  ]);
  kaplayContext.add([
    kaplayContext.text("Controls", { size: 50, font: ROUND_FONT }),
    // we have to use the "area" component, because later we want to use the "anchor" component
    kaplayContext.area(),
    // the "anchor" component cannot be used without the "area" component
    kaplayContext.anchor("center"),
    kaplayContext.pos(kaplayContext.center().x, kaplayContext.center().y - 200),
  ]);

  // the "controlsPrompts" is an invisible game object which serves as a parent for the controls objects
  // the child objects will be visible
  const controlsPrompts = kaplayContext.add([
    kaplayContext.pos(kaplayContext.center().x + 30, kaplayContext.center().y),
  ]);
  controlsPrompts.add([
    kaplayContext.sprite(KEY_CONTROL_SPRITE.arrowUp),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(0, -80),
  ]);
  controlsPrompts.add([kaplayContext.sprite(KEY_CONTROL_SPRITE.arrowDown)]);
  controlsPrompts.add([
    kaplayContext.sprite(KEY_CONTROL_SPRITE.arrowLeft),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(-80, 0),
  ]);
  controlsPrompts.add([
    kaplayContext.sprite(KEY_CONTROL_SPRITE.arrowRight),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(80, 0),
  ]);
  controlsPrompts.add([
    kaplayContext.sprite(KEY_CONTROL_SPRITE.space),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(-200, 0),
  ]);
  controlsPrompts.add([
    kaplayContext.text("Jump", { size: 32, font: ROUND_FONT }),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(-190, 100),
  ]);
  controlsPrompts.add([
    kaplayContext.text("Move", { size: 32, font: ROUND_FONT }),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(10, 100),
  ]);

  displayBlinkingMessage(
    "Press [ Enter ] to start the game",
    kaplayContext.vec2(
      kaplayContext.center().x,
      kaplayContext.center().y + 220,
    ),
  );

  kaplayContext.onKeyPress(ENTER_KEY, () => {
    kaplayContext.play(SOUND.confirmUi, { speed: 1.5 });
    kaplayContext.go(SCENE.firstLevel);
  });
};
