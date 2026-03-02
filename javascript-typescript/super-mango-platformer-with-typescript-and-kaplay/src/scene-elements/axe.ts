import type { GameObj } from "kaplay";
import { AXE_STATE, SCENE_ELEMENT_SPRITE, SOUND, TAG } from "../constants";
import kaplayContext from "../kaplay-context";
import type { AxeConfig } from "../level-content/models";

// the function creates an array of axes depending on the axe configs passed as an argument
export const createAxes = (axeConfigs: AxeConfig[]) => {
  for (const config of axeConfigs) {
    const { position, swingDuration } = config;

    const axeObject = kaplayContext.add([
      kaplayContext.sprite(SCENE_ELEMENT_SPRITE.axe),
      kaplayContext.scale(4),
      kaplayContext.pos(position),
      kaplayContext.area({
        /*
         * With the "shape" field we specify dimensions of a hit box and where it will be located.
         *
         * The first argument of the "Rect" defines the position of the hitbox -> we want it to be 40 pixels
         * lower as is the original position of an axe game object.
         */
        shape: new kaplayContext.Rect(kaplayContext.vec2(0, 40), 30, 10),
        collisionIgnore: [TAG.spider, TAG.flame],
      }),
      // the "anchor()" component can receive specific coordinates where a game object should be anchored
      kaplayContext.anchor(kaplayContext.vec2(0, -0.75)),
      // we need to add the "rotate()" component because we want to be able to rotate the game object later
      kaplayContext.rotate(),
      kaplayContext.state(AXE_STATE.swingLeft, [
        AXE_STATE.swingLeft,
        AXE_STATE.swingRight,
      ]),
      kaplayContext.offscreen(),
      TAG.axe,
      // custom properties specific to a spider game object
      {
        async swing(this: GameObj, targetAngle: number) {
          if (!this.isOffScreen()) {
            kaplayContext.play(SOUND.swingingAxe);
          }

          await kaplayContext.tween(
            // the "angle" field is available on a game object because we used the "rotate()" component
            this.angle,
            targetAngle,
            swingDuration,
            (newAngle) => (this.angle = newAngle),
            kaplayContext.easings.easeInOutSine,
          );
        },

        setMovementPattern(this: GameObj) {
          const swingLeftState = this.onStateEnter(
            AXE_STATE.swingLeft,
            async () => {
              await this.swing(90);
              this.enterState(AXE_STATE.swingRight);
            },
          );

          const swingRightState = this.onStateEnter(
            AXE_STATE.swingRight,
            async () => {
              await this.swing(-90);
              this.enterState(AXE_STATE.swingLeft);
            },
          );

          // when an axe game object is out of the screen, we want its sounds to stop playing
          kaplayContext.onSceneLeave(() => {
            swingLeftState.cancel();
            swingRightState.cancel();
          });
        },
      },
    ]);

    axeObject.setMovementPattern();
  }
};
