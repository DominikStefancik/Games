import type { GameObj, Vec2 } from "kaplay";
import { BIRD_ANIMATION, BIRD_STATE, SOUND, TAG } from "../constants";
import kaplayContext from "../kaplay-context";
import type { BirdConfig } from "../level-content/models";

// the function creates an array of birds depending on the bird configs passed as an argument
export const createBirds = (birdConfigs: BirdConfig[]) => {
  for (const config of birdConfigs) {
    const { type, position, movementRange, speed } = config;

    const birdObject = kaplayContext.add([
      kaplayContext.sprite(`bird${type}`, { anim: BIRD_ANIMATION.fly }),
      kaplayContext.scale(4),
      kaplayContext.pos(position),
      kaplayContext.area({
        shape: new kaplayContext.Rect(kaplayContext.vec2(0), 10, 10),
      }),
      kaplayContext.anchor("center"),
      kaplayContext.rotate(),
      kaplayContext.state(BIRD_STATE.flyLeft, [
        BIRD_STATE.flyLeft,
        BIRD_STATE.flyRight,
        BIRD_STATE.diveAttackLeft,
        BIRD_STATE.diveAttackRight,
      ]),
      kaplayContext.offscreen(),
      TAG.bird,
      // custom properties specific to a spider game object
      {
        async fly(this: GameObj, isDirectionLeft: boolean) {
          await kaplayContext.tween(
            this.pos.y,
            this.pos.y + movementRange * (isDirectionLeft ? -1 : 1),
            speed,
            (newPositionY) => (this.pos.y = newPositionY),
            kaplayContext.easings.linear,
          );
        },

        async diveAttack(this: GameObj, targetPosition: Vec2) {
          if (!this.isOffScreen()) {
            kaplayContext.play(SOUND.dive, { volume: 0.02 });
          }

          await kaplayContext.tween(
            this.pos,
            targetPosition,
            speed,
            (newPosition) => (this.pos = newPosition),
            kaplayContext.easings.easeInSine,
          );
        },

        setMovementPattern(this: GameObj) {
          const flyLeftState = this.onStateEnter(
            BIRD_STATE.flyLeft,
            async () => {
              this.flipX = false;
              await this.fly(true);
              this.enterState(BIRD_STATE.diveAttackLeft);
            },
          );

          const flyRightState = this.onStateEnter(
            BIRD_STATE.flyRight,
            async () => {
              this.flipX = true;
              await this.fly(false);
              this.enterState(BIRD_STATE.diveAttackRight);
            },
          );

          const diveAttackLeftState = this.onStateEnter(
            BIRD_STATE.diveAttackLeft,
            async () => {
              // first a bird dives down
              await this.diveAttack(
                kaplayContext.vec2(
                  this.pos.x - movementRange,
                  this.pos.y + movementRange,
                ),
              );
              // then it goes up
              await this.diveAttack(
                kaplayContext.vec2(
                  this.pos.x - movementRange,
                  this.pos.y - movementRange,
                ),
              );
              this.enterState(BIRD_STATE.flyRight);
            },
          );

          const diveAttackRightState = this.onStateEnter(
            BIRD_STATE.diveAttackRight,
            async () => {
              // first a bird dives down
              await this.diveAttack(
                kaplayContext.vec2(
                  this.pos.x + movementRange,
                  this.pos.y + movementRange,
                ),
              );
              // then it goes up
              await this.diveAttack(
                kaplayContext.vec2(
                  this.pos.x + movementRange,
                  this.pos.y - movementRange,
                ),
              );
              this.enterState(BIRD_STATE.flyLeft);
            },
          );

          // when we leave a scene we want all actions associated with flame's state to be canceled
          kaplayContext.onSceneLeave(() => {
            flyLeftState.cancel();
            flyRightState.cancel();
            diveAttackLeftState.cancel();
            diveAttackRightState.cancel();
          });
        },
      },
    ]);

    birdObject.setMovementPattern();
  }
};
