import type { GameObj } from "kaplay";
import { FISH_ANIMATION, FISH_STATE, TAG } from "../constants";
import kaplayContext from "../kaplay-context";
import type { FishConfig } from "../level-content/models";

// the function creates an array of fish depending on the fish configs passed as an argument
export const createFish = (fishConfigs: FishConfig[]) => {
  for (const config of fishConfigs) {
    const { type, position, movementRange } = config;

    const fishObject = kaplayContext.add([
      kaplayContext.sprite(`fish${type}`, { anim: FISH_ANIMATION.jump }),
      kaplayContext.scale(4),
      kaplayContext.rotate(90),
      kaplayContext.pos(position),
      kaplayContext.area({
        shape: new kaplayContext.Rect(kaplayContext.vec2(0), 12, 12),
      }),
      kaplayContext.anchor("center"),
      kaplayContext.state(FISH_STATE.jumpUp, [
        FISH_STATE.jumpUp,
        FISH_STATE.fall,
      ]),
      kaplayContext.offscreen(),
      TAG.fish,
      // custom properties specific to a spider game object
      {
        setMovementPattern(this: GameObj) {
          const jumpUpState = this.onStateEnter(FISH_STATE.jumpUp, async () => {
            this.flipX = false;
            await kaplayContext.tween(
              this.pos.y,
              // if the fish goes up, the value of Y-coordinate decreaces
              this.pos.y - movementRange,
              2,
              (newPositionY) => (this.pos.y = newPositionY),
              kaplayContext.easings.easeOutSine,
            );
            this.enterState(FISH_STATE.fall);
          });

          const fallState = this.onStateEnter(FISH_STATE.fall, async () => {
            this.flipX = true;
            await kaplayContext.tween(
              this.pos.y,
              // if the fish goes down, the value of Y-coordinate increaces
              this.pos.y + movementRange,
              2,
              (newPositionY) => (this.pos.y = newPositionY),
              kaplayContext.easings.easeOutSine,
            );
            this.enterState(FISH_STATE.jumpUp);
          });

          // when we leave a scene we want all actions associated with fish' state to be canceled
          kaplayContext.onSceneLeave(() => {
            jumpUpState.cancel();
            fallState.cancel();
          });
        },
      },
    ]);

    fishObject.setMovementPattern();
  }
};
