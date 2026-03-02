import type { GameObj } from "kaplay";
import { SAW_STATE, SCENE_ELEMENT_SPRITE, SOUND, TAG } from "../constants";
import kaplayContext from "../kaplay-context";
import type { SawConfig } from "../level-content/models";

// the function creates an array of saws depending on the saw configs passed as an argument
export const createSaws = (sawConfigs: SawConfig[]) => {
  for (const config of sawConfigs) {
    const { position, movementRange } = config;

    const sawObject = kaplayContext.add([
      kaplayContext.sprite(SCENE_ELEMENT_SPRITE.saw),
      kaplayContext.scale(4),
      kaplayContext.pos(position),
      kaplayContext.area(),
      kaplayContext.anchor("center"),
      // we need to add the "rotate()" component because we want to be able to rotate the game object later
      kaplayContext.rotate(),
      kaplayContext.state(SAW_STATE.rotateLeft, [
        SAW_STATE.rotateLeft,
        SAW_STATE.rotateRight,
      ]),
      kaplayContext.offscreen(),
      TAG.saw,
      // custom properties specific to a spider game object
      {
        async moveAndRotate(this: GameObj, isDirectionLeft: boolean) {
          if (!this.isOffScreen()) {
            kaplayContext.play(SOUND.saw, { volume: 0.4, seek: 10 });
          }

          await Promise.all([
            kaplayContext.tween(
              this.pos.x,
              this.pos.x + movementRange * (isDirectionLeft ? -1 : 1),
              1,
              (newPosition) => (this.pos.x = newPosition),
              kaplayContext.easings.linear,
            ),
            kaplayContext.tween(
              // the "angle" field is available on a game object because we used the "rotate()" component
              this.angle,
              360,
              2,
              (newAngle) => (this.angle = newAngle),
              kaplayContext.easings.linear,
            ),
          ]);
        },

        setMovementPattern(this: GameObj) {
          const rotateLeftState = this.onStateEnter(
            SAW_STATE.rotateLeft,
            async () => {
              await this.moveAndRotate(true);
              this.angle = 0;
              this.enterState(SAW_STATE.rotateRight);
            },
          );

          const rotateRightState = this.onStateEnter(
            SAW_STATE.rotateRight,
            async () => {
              await this.moveAndRotate(false);
              this.angle = 0;
              this.enterState(SAW_STATE.rotateLeft);
            },
          );

          // when a saw game object is out of the screen, we want its sounds to stop playing
          kaplayContext.onSceneLeave(() => {
            rotateLeftState.cancel();
            rotateRightState.cancel();
          });
        },
      },
    ]);

    sawObject.setMovementPattern();
  }
};
