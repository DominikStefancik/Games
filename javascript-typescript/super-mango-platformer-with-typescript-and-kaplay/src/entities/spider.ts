import type { Collision, GameObj } from "kaplay";
import { SOUND, SPIDER_ANIMATION, SPIDER_STATE, TAG } from "../constants";
import kaplayContext from "../kaplay-context";
import type { SpiderConfig } from "../level-content/models";

// the function creates an array of spiders depending on the spider configs passed as an argument
export const createSpiders = (spiderConfigs: SpiderConfig[]) => {
  for (const config of spiderConfigs) {
    const { type, position, movementRange, speed } = config;

    const spiderObject = kaplayContext.add([
      kaplayContext.sprite(`spider${type}`, { anim: SPIDER_ANIMATION.crawl }),
      kaplayContext.scale(4),
      kaplayContext.pos(position),
      kaplayContext.area({
        shape: new kaplayContext.Rect(kaplayContext.vec2(0, 4.5), 20, 6),
        // ignore collisions with other spiders
        collisionIgnore: [TAG.spider],
      }),
      kaplayContext.body(),
      kaplayContext.anchor("center"),
      kaplayContext.state(SPIDER_STATE.idle, [
        SPIDER_STATE.idle,
        SPIDER_STATE.crawlLeft,
        SPIDER_STATE.crawlRight,
      ]),
      kaplayContext.offscreen(),
      TAG.spider,
      // custom properties specific to a spider game object
      {
        async crawl(this: GameObj, isDirectionLeft: boolean) {
          if (this.getCurAnim()?.name !== SPIDER_ANIMATION.crawl) {
            this.play(SPIDER_ANIMATION.crawl);
          }

          await kaplayContext.tween(
            this.pos.x,
            this.pos.x + movementRange * (isDirectionLeft ? -1 : 1),
            speed,
            (newPositionX) => (this.pos.x = newPositionX),
            kaplayContext.easings.easeOutSine,
          );
        },

        setMovementPattern(this: GameObj) {
          const idleState = this.onStateEnter(
            SPIDER_STATE.idle,
            async (previousState: string) => {
              if (this.getCurAnim()?.name !== SPIDER_ANIMATION.idle) {
                this.play(SPIDER_ANIMATION.idle);
              }

              await kaplayContext.wait(1);

              if (previousState === SPIDER_STATE.crawlLeft) {
                this.enterState(SPIDER_STATE.crawlRight);
                return;
              }

              // the previous state is undefined, because we just entered the "idle" state
              if (!previousState || previousState == SPIDER_STATE.crawlRight) {
                // the "jump" method is provided by the Kaplay
                this.jump();
              }

              this.enterState(SPIDER_STATE.crawlLeft);

              // the "isOffScreen" method is provided by the Kaplay, because we used the "isOffScreen()" component
              if (!this.isOffScreen()) {
                kaplayContext.play(SOUND.spiderAttack, { volume: 0.6 });
              }
            },
          );

          const crawlLeftState = this.onStateEnter(
            SPIDER_STATE.crawlLeft,
            async () => {
              this.flipX = false;
              await this.crawl(true);
              // the second parameter represents the previous state
              this.enterState(SPIDER_STATE.idle, SPIDER_STATE.crawlLeft);
            },
          );

          const crawlRightState = this.onStateEnter(
            SPIDER_STATE.crawlRight,
            async () => {
              this.flipX = true;
              await this.crawl(false);
              // the second parameter represents the previous state
              this.enterState(SPIDER_STATE.idle, SPIDER_STATE.crawlRight);
            },
          );

          // when we leave a scene we want all actions associated with spider's state to be canceled
          kaplayContext.onSceneLeave(() => {
            idleState.cancel();
            crawlLeftState.cancel();
            crawlRightState.cancel();
          });
        },

        enablePassthrough(this: GameObj) {
          /*
           * The "onBeforePhysicsResolve()" method is available because the game object has the "body" component
           * The method runs before a collision with another game object would be resolved.
           * Using it is one way to intercept the collision.
           *
           */
          this.onBeforePhysicsResolve((collision: Collision) => {
            if (collision.target.is(TAG.passthrough) && this.isJumping()) {
              // ignore collistion and allow jump on a platform from below
              collision.preventResolution();
            }
          });
        },
      },
    ]);

    spiderObject.setMovementPattern();
    spiderObject.enablePassthrough();
  }
};
