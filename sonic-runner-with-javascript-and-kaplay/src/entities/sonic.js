import {
  ANIMATION_JUMP,
  ANIMATION_RUN,
  BUTTON_JUMP,
  JUMP_SOUND_ID,
  SONIC_SPRITE_ID,
} from "../constants";
import kaplayContext from "../kaplay-context";

// create the Sonic game object
// the "position" parameter is Vec2 object
export const createSonic = (position) => {
  const sonicObject = kaplayContext.add([
    kaplayContext.sprite(SONIC_SPRITE_ID, { anim: ANIMATION_RUN }), // "anim" defines a default animation
    kaplayContext.scale(4),
    // adds an automatic hit box (i.e. a collider area) for the object
    // you an also specify a shape (as an argumnet) this hit box will have
    kaplayContext.area(),
    // "anchor" allows you to change the origin of the game object
    kaplayContext.anchor("center"),
    kaplayContext.pos(position),
    // "jumpForce" flag defines how much a game object will jump
    kaplayContext.body({ jumpForce: 1700 }),

    // here we will define custom properties for a game object
    {
      // "setControls() {}" is a shortcut for "setControls: () => {}"
      setControls() {
        kaplayContext.onButtonPress(BUTTON_JUMP, () => {
          // "this" represents the "sonicObject"
          // "isGrounded" is method added by the "body" component
          // if the Sonic object is on the platform
          if (this.isGrounded()) {
            // "play" is method added by the "sprite" component
            // play the "jump" animation
            this.play(ANIMATION_JUMP);
            // "jump" is method added by the "sprite" component
            this.jump();
            // play the sound of jumping
            kaplayContext.play(JUMP_SOUND_ID, { volume: 0.5 });
          }
        });
      },
      setEvents() {
        this.onGround(() => {
          // when the Sonic object is again on the ground after jumping
          // play the "run" animation
          this.play(ANIMATION_RUN);
        });
      },
    },
  ]);

  return sonicObject;
};
