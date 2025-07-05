import type { KAPLAYCtx } from "kaplay";
import { BACKGROUND_LAYER_1_ID, BACKGROUND_LAYER_2_ID } from "./constants";
import kaplayContext from "./kaplay-context";

export const arena = (context: KAPLAYCtx) => {
  context.loadSprite(
    BACKGROUND_LAYER_1_ID,
    "./assets/graphics/background/background_layer_1.png",
  );
  context.loadSprite(
    BACKGROUND_LAYER_2_ID,
    "./assets/graphics/background/background_layer_2.png",
  );

  // the output of calling the "add()" method is a game object
  context.add([
    context.sprite(BACKGROUND_LAYER_1_ID),
    kaplayContext.pos(0, 0),
    kaplayContext.scale(4),
    // the game object will stay fixed regardaless of how camera moves
    kaplayContext.fixed(),
  ]);
  context.add([
    context.sprite(BACKGROUND_LAYER_2_ID),
    kaplayContext.pos(0, 0),
    kaplayContext.scale(4),
    // the game object will stay fixed regardaless of how camera moves
    kaplayContext.fixed(),
  ]);
};
