import { ANIMATION_RUN, SONIC_SPRITE_ID } from "../constants";
import kaplayContext from "../kaplay-context";

// create the Sonic game object
// the "position" parameter is Vec2 object
export const createSonic = (position) => {
  kaplayContext.add([
    kaplayContext.sprite(SONIC_SPRITE_ID, { anim: ANIMATION_RUN }), // "anim" defines a default animation
    kaplayContext.scale(4),
    // adds an automatic hit box (i.e. a collider area) for the object
    // you an also specify a shape (as an argumnet) this hit box will have
    kaplayContext.area(),
    // "anchor" allows you to change the origin of the game object
    kaplayContext.anchor("center"),
    kaplayContext.pos(position),
  ]);
};
