import type { GameObj, KAPLAYCtx, Vec2 } from "kaplay";
import {
  IDLE_ANIMATION_ID,
  NINJA_SPRITE_ID,
  NINJA_TAG,
  SAMURAI_TAG,
} from "../constants";
import { initialFighterProps, setFighterControls } from "./fighter";

export const createNinja = (params: {
  context: KAPLAYCtx;
  parentObject: GameObj;
  position: Vec2;
}): GameObj => {
  const { context, parentObject, position } = params;

  const gameObject = parentObject.add([
    context.sprite(NINJA_SPRITE_ID, { anim: IDLE_ANIMATION_ID }),
    context.pos(position),
    context.area({
      shape: new context.Rect(context.vec2(0, 5), 20, 40),
      // the set of game objects for which collision with the Ninja object will be ignored
      collisionIgnore: [SAMURAI_TAG],
    }),
    context.anchor("center"),
    // makes a game object susceptible to gravity and physics
    context.body(),
    // allows us to track "health" of a game object
    context.health(initialFighterProps.maxHealthPoints),
    context.opacity(),
    // this id added for identification of the Ninja game object
    NINJA_TAG,

    // here we will define custom properties for a game object
    {
      ...initialFighterProps,
      setControls: () => {
        setFighterControls({
          context,
          fighter: gameObject,
          keys: {
            LEFT: "left",
            RIGHT: "right",
            UP: "up",
            DOWN: "down",
          },
        });
      },
    },
  ]);

  return gameObject;
};
