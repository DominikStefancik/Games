import { ANIMATION_SPIN, RING_SPRITE_ID, TAG_RING } from "../constants";
import kaplayContext from "../kaplay-context";

// create the Ring game object
// the "position" parameter is Vec2 object
export const createRing = (position) => {
  const ringObject = kaplayContext.add([
    kaplayContext.sprite(RING_SPRITE_ID, { anim: ANIMATION_SPIN }), // "anim" defines a default animation
    kaplayContext.scale(4),
    // adds an automatic hit box (i.e. a collider area) for the object
    // you an also specify a custom shape (as an argument) this hit box will have
    kaplayContext.area(),
    // "anchor" allows you to change the origin of the game object
    kaplayContext.anchor("center"),
    kaplayContext.pos(position),
    // "offscreen" method adds more components which we can check if the game object is offscreen
    kaplayContext.offscreen(),
    // tag used to identify a game object
    // tags are gonna be used in colliders and event listeners
    TAG_RING,
  ]);

  return ringObject;
};
