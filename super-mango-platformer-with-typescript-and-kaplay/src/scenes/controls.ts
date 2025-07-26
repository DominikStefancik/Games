import {
  ARROW_DOWN_KEY_SPRITE,
  ARROW_LEFT_KEY_SPRITE,
  ARROW_RIGHT_KEY_SPRITE,
  ARROW_UP_KEY_SPRITE,
  CONFIRM_UI_SOUND,
  ENTER_KEY,
  FIRST_LEVEL_SCENE,
  FOREST_BACKGROUND_SPRITE,
  ROUND_FONT,
  SPACE_KEY_SPRITE,
} from "../constants";
import kaplayContext from "../kaplay-context";
import { displayBlinkingMessage } from "./helpers";

export const controls = () => {
  kaplayContext.add([
    kaplayContext.sprite(FOREST_BACKGROUND_SPRITE),
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
    kaplayContext.sprite(ARROW_UP_KEY_SPRITE),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(0, -80),
  ]);
  controlsPrompts.add([kaplayContext.sprite(ARROW_DOWN_KEY_SPRITE)]);
  controlsPrompts.add([
    kaplayContext.sprite(ARROW_LEFT_KEY_SPRITE),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(-80, 0),
  ]);
  controlsPrompts.add([
    kaplayContext.sprite(ARROW_RIGHT_KEY_SPRITE),
    // the position of a child game object is relative to its parent game object
    kaplayContext.pos(80, 0),
  ]);
  controlsPrompts.add([
    kaplayContext.sprite(SPACE_KEY_SPRITE),
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
    kaplayContext.play(CONFIRM_UI_SOUND, { speed: 1.5 });
    kaplayContext.go(FIRST_LEVEL_SCENE);
  });
};
