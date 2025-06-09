import { ANIMATION_RUN, MOTOBUG_SPRITE_ID, TAG_ENEMY } from "../constants";
import kaplayContext from "../kaplay-context";

// create the Motobug game object
// the "position" parameter is Vec2 object
export const createMotobug = (position) => {
  const motobugObject = kaplayContext.add([
    kaplayContext.sprite(MOTOBUG_SPRITE_ID, { anim: ANIMATION_RUN }), // "anim" defines a default animation
    kaplayContext.scale(4),
    // adds an automatic hit box (i.e. a collider area) for the object
    // you an also specify a custom shape (as an argumnet) this hit box will have
    kaplayContext.area({
      // the first argument of "Rect" is a position of the hitbox relative to the game object
      shape: new kaplayContext.Rect(kaplayContext.vec2(-5, 0), 32, 32),
    }),
    // "anchor" allows you to change the origin of the game object
    kaplayContext.anchor("center"),
    kaplayContext.pos(position),
    // "offscreen" method adds more components which we can check if the game object is offscreen
    kaplayContext.offscreen(),
    // tag used to identify a game object
    // tags are gonna be used in colliders and event listeners
    TAG_ENEMY,
  ]);

  return motobugObject;
};
