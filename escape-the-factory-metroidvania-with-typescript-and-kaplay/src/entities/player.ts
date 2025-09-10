import type { Collision, GameObj, KEventController, Vec2 } from "kaplay";
import {
  ANIMATION,
  COLLIDER_TYPE,
  ENTITY_SPRITE,
  KEY_CONTROL,
  TAG,
} from "../constants";
import kaplayContext from "../kaplay-context";
import { state } from "../state/globalStateManager";

export const createPlayer = (): GameObj => {
  // the method "make()" from Kaplay creates a game object, but doesn't make it visible
  // later we can take the game object and pass it to the Kaplay method "add" to add it to a scene and make it visible
  return kaplayContext.make([
    kaplayContext.sprite(ENTITY_SPRITE.player, { anim: ANIMATION.player.idle }),
    // we need to explicitly add the "pos" component, because later we want to change the player's position
    kaplayContext.pos(),
    // by adding the "area" component we create a hitbox for a player which then will be able to react to
    // collitions with other game objects
    kaplayContext.area({
      shape: new kaplayContext.Rect(kaplayContext.vec2(0, 18), 12, 12),
    }),
    kaplayContext.anchor("center"),
    // the "body" component will ensure that a game object is susceptible to gravity
    kaplayContext.body({ mass: 100, jumpForce: 320 }),
    // the "doubleJump" component allows to implement multiple jumps for a game objects
    // (it doesn't have to be only a double-jump)
    // Note: initially we set the number of jumps to 1, and then later increase it
    kaplayContext.doubleJump(state.getState().isDoubleJumpUnlocked ? 2 : 1),
    kaplayContext.opacity(),
    kaplayContext.health(state.getState().playerHealthPoints),
    TAG.player,
    {
      speed: 150,
      isAttacking: false,
      // we want to keep a list of control handlers so later we can cancel then all (when a player dies)
      controlHandlers: [],
      setControls(this: GameObj) {
        this.controlHandlers.push(createKeyPressHandler(this));
        this.controlHandlers.push(createKeyDownHandler(this));
        this.controlHandlers.push(createKeyReleaseHandler(this));
      },
      disableControls(this: GameObj) {
        for (const handler of this.controlHandlers) {
          handler.cancel();
        }
      },
      respawnIfOutOfBounds(
        boundValue: number,
        destinationName: string,
        previousSceneData = { exitName: null },
      ) {},
      setPosition(this: GameObj, position: Vec2) {
        this.pos = position;
      },
      setEvents(this: GameObj) {
        // the method "onFall" from Kaplay checks if a game object starts falling after jumping
        this.onFall(() => {
          this.play(ANIMATION.player.fall);
        });

        // the method "onFallOff" from Kaplay checks if a game object falls off a platform
        this.onFallOff(() => {
          this.play(ANIMATION.player.fall);
        });

        // the method "onGround" from Kaplay checks if a game object is grounded
        this.onGround(() => {
          this.play(ANIMATION.player.idle);
        });

        // the method "onGround" from Kaplay checks if a game object bumps into something on the head
        this.onHeadbutt(() => {
          this.play(ANIMATION.player.fall);
        });
      },
      enablePassthrough(this: GameObj) {
        // the method "onBeforePhysicsResolve" from Kaplay is an event handler
        // that runs before a collision would be resolved
        this.onBeforePhysicsResolve((collision: Collision) => {
          if (
            collision.target.is(COLLIDER_TYPE.passthrough) &&
            this.isJumping()
          ) {
            // the method "preventResolution" makes sure that a collision is ignored
            collision.preventResolution();
          }
        });
      },
    },
  ]);
};

const createKeyPressHandler = (player: GameObj): KEventController => {
  return kaplayContext.onKeyPress((key) => {
    if (key === KEY_CONTROL.up) {
      if (player.getCurAnim()?.name !== ANIMATION.player.jump) {
        player.play(ANIMATION.player.jump);
        player.doubleJump();
      }
    }

    if (
      key === KEY_CONTROL.space &&
      player.getCurAnim()?.name !== ANIMATION.player.attack &&
      player.isGrounded()
    ) {
      player.isAttacking = true;
      // when attacking, we create an invisible hitbox. If an enemy collides with this inbox,
      // it will receive damage
      player.add([
        kaplayContext.pos(player.flipX ? -25 : 0, 10),
        kaplayContext.area({
          shape: new kaplayContext.Rect(kaplayContext.vec2(0), 25, 10),
        }),
        TAG["sword-hitbox"],
      ]);

      player.play(ANIMATION.player.attack);

      // event listener when an animation ends
      player.onAnimEnd((animation: string) => {
        // at the and of the player attack animation, we need to destroy the sword hitbox we created
        if (animation === ANIMATION.player.attack) {
          const swordHitBox = kaplayContext.get(TAG["sword-hitbox"], {
            recursive: true,
          })[0];

          if (swordHitBox) {
            kaplayContext.destroy(swordHitBox);
          }

          player.isAttacking = false;
          player.play(ANIMATION.player.idle);
        }
      });
    }
  });
};

const createKeyDownHandler = (player: GameObj): KEventController => {
  return kaplayContext.onKeyDown((key) => {
    if (key === KEY_CONTROL.left && !player.isAttacking) {
      if (
        player.getCurAnim()?.name !== ANIMATION.player.run &&
        player.isGrounded()
      ) {
        player.play(ANIMATION.player.run);
      }

      player.flipX = true;
      // the method "move()" from Kaplay moves the game object with given amount of pixels in x and y coordinate
      player.move(-player.speed, 0);
    }

    if (key === KEY_CONTROL.right && !player.isAttacking) {
      if (
        player.getCurAnim()?.name !== ANIMATION.player.run &&
        player.isGrounded()
      ) {
        player.play(ANIMATION.player.run);
      }

      player.flipX = false;
      // the method "move()" from Kaplay moves the game object with given amount of pixels in x and y coordinate
      player.move(player.speed, 0);
    }
  });
};

const createKeyReleaseHandler = (player: GameObj): KEventController => {
  return kaplayContext.onKeyRelease(() => {
    if (
      ![
        ANIMATION.player.idle,
        ANIMATION.player.jump,
        ANIMATION.player.fall,
        ANIMATION.player.attack,
      ].includes(player.getCurAnim()?.name)
    ) {
      player.play(ANIMATION.player.idle);
    }
  });
};
