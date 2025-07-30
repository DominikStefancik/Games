import type { GameObj } from "kaplay";
import { FLAME_ANIMATION, FLAME_STATE, TAG } from "../constants";
import kaplayContext from "../kaplay-context";
import type { FlameConfig } from "../level-content/models";

// the function creates an array of flames depending on the flame configs passed as an argument
export const createFlames = (flameConfigs: FlameConfig[]) => {
  for (const config of flameConfigs) {
    const { type, position, movementRange } = config;

    const flameObject = kaplayContext.add([
      kaplayContext.sprite(`flame${type}`, { anim: FLAME_ANIMATION.jump }),
      kaplayContext.scale(4),
      kaplayContext.pos(position),
      kaplayContext.area({
        shape: new kaplayContext.Rect(kaplayContext.vec2(0), 12, 12),
      }),
      kaplayContext.anchor("center"),
      kaplayContext.state(FLAME_STATE.jumpUp, [
        FLAME_STATE.jumpUp,
        FLAME_STATE.fall,
      ]),
      kaplayContext.offscreen(),
      TAG.flame,
      // custom properties specific to a spider game object
      {
        setMovementPattern(this: GameObj) {
          const jumpUpState = this.onStateEnter(
            FLAME_STATE.jumpUp,
            async () => {
              this.flipY = false;
              await kaplayContext.tween(
                this.pos.y,
                // if the flame goes up, the value of Y-coordinate decreaces
                this.pos.y - movementRange,
                2,
                (newPositionY) => (this.pos.y = newPositionY),
                kaplayContext.easings.easeOutSine,
              );
              this.enterState(FLAME_STATE.fall);
            },
          );

          const fallState = this.onStateEnter(FLAME_STATE.fall, async () => {
            this.flipY = true;
            await kaplayContext.tween(
              this.pos.y,
              // if the flame goes down, the value of Y-coordinate increaces
              this.pos.y + movementRange,
              2,
              (newPositionY) => (this.pos.y = newPositionY),
              kaplayContext.easings.easeOutSine,
            );
            this.enterState(FLAME_STATE.jumpUp);
          });

          // when we leave a scene we want all actions associated with flame's state to be canceled
          kaplayContext.onSceneLeave(() => {
            jumpUpState.cancel();
            fallState.cancel();
          });
        },
      },
    ]);

    flameObject.setMovementPattern();
  }
};
