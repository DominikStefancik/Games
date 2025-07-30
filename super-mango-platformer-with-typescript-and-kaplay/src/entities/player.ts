import type { Collision, GameObj } from "kaplay";
import kaplayContext from "../kaplay-context";
import {
  ENTITY_SPRITE,
  KEY_CONTROL,
  PLAYER_ANIMATION,
  SCENE,
  SOUND,
  TAG,
} from "../constants";
import type { LevelConfig } from "../level-content/models";

export const createPlayer = (levelConfig: LevelConfig): GameObj => {
  const {
    playerStartPosition,
    playerSpeed,
    jumpForce,
    playerLivesCount,
    lostLiveLevel,
    currentLevelScene,
    isInLastLeveL,
  } = levelConfig;

  const playerObject = kaplayContext.add([
    kaplayContext.sprite(ENTITY_SPRITE.player, {
      anim: PLAYER_ANIMATION.idle,
    }),
    kaplayContext.scale(4),
    kaplayContext.area({
      shape: new kaplayContext.Rect(kaplayContext.vec2(0, 3), 8, 8),
    }),
    kaplayContext.body(),
    kaplayContext.pos(playerStartPosition),
    kaplayContext.anchor("center"),
    TAG.player,
    // custom properties specific to a player game object
    {
      lives: playerLivesCount,
      currentLevelScene,
      isRespawning: false,
      previousHeight: playerStartPosition.y,
      heightDelta: 0,
      isMoving: false,
      timeSinceLastGrounded: 0,
      coyoteLapse: 0.1,
      hasJumpedOnce: false,
      collectedCoinCount: 0,
      isInLastLeveL,
      setControls(this: GameObj) {
        kaplayContext.onKeyDown(KEY_CONTROL.left, () => {
          if (this.getCurAnim()?.name !== PLAYER_ANIMATION.run) {
            this.play(PLAYER_ANIMATION.run);
          }
          this.flipX = true;

          // if  the player is respowning, don't react to a key press
          if (!this.isRespawning) {
            // the "move()" method is from Kaplay and it moves a game object in a vertical and horizontal direction
            this.move(-playerSpeed, 0);
            this.isMoving = true;
          }
        });

        kaplayContext.onKeyDown(KEY_CONTROL.right, () => {
          if (this.getCurAnim()?.name !== PLAYER_ANIMATION.run) {
            this.play(PLAYER_ANIMATION.run);
          }
          this.flipX = false;

          // if  the player is respowning, don't react to a key press
          if (!this.isRespawning) {
            // the "move()" method is from Kaplay and it moves a game object in a vertical and horizontal direction
            this.move(playerSpeed, 0);
            this.isMoving = true;
          }
        });

        kaplayContext.onKeyDown(KEY_CONTROL.space, () => {
          // the "isGrounded()" method is from Kaplay and it checks if a game object is on a platform
          const isOnGroundAndCanJump = this.isGrounded() && !this.isRespawning;
          const isOnTheEdgeAndCanJump =
            !this.isGrounded() &&
            kaplayContext.time() - this.timeSinceLastGrounded <
              this.coyoteLapse &&
            !this.hasJumpedOnce;

          if (isOnGroundAndCanJump || isOnTheEdgeAndCanJump) {
            // the "jump()" method is from Kaplay and it jumps a game object in a vertical and horizontal direction
            this.jump(jumpForce);
            kaplayContext.play(SOUND.jump);
            this.hasJumpedOnce = true;
          }
        });

        kaplayContext.onKeyRelease(
          [KEY_CONTROL.left, KEY_CONTROL.right],
          () => {
            this.play(PLAYER_ANIMATION.idle);
            this.isMoving = false;
          },
        );
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

          if (
            collision.target.is(TAG.passthrough) &&
            kaplayContext.isKeyDown(KEY_CONTROL.down)
          ) {
            // ignore collistion and allow jump on a platform from below
            collision.preventResolution();
          }
        });
      },

      enableCoinPickup(this: GameObj) {
        // the "coin" paramater represents a coin game object the player collided with
        this.onCollide(TAG.coin, (coin: GameObj) => {
          this.collectedCoinCount++;
          kaplayContext.destroy(coin);
          kaplayContext.play(SOUND.coin);
        });
      },

      enableCreatureAndItemVulnerability(this: GameObj) {
        const playSoundAndRespawn = () => {
          kaplayContext.play(SOUND.hit, { speed: 1.5 });
          this.respawnPlayer();
        };

        this.onCollide(TAG.spider, playSoundAndRespawn);
        this.onCollide(TAG.fish, playSoundAndRespawn);
        this.onCollide(TAG.flame, playSoundAndRespawn);
        this.onCollide(TAG.axe, playSoundAndRespawn);
      },

      respawnPlayer(this: GameObj) {
        if (this.lives > 0) {
          this.lives--;
          this.pos = playerStartPosition;
          this.isRespawning = true;
          kaplayContext.wait(1, () => (this.isRespawning = false));
        }

        if (this.lives === 0) {
          kaplayContext.go(SCENE.gameOver);
        }
      },

      update(this: GameObj) {
        kaplayContext.onUpdate(() => {
          if (this.isGrounded()) {
            this.hasJumpedOnce = false;
            this.timeSinceLastGrounded = kaplayContext.time();
          }

          this.heightDelta = this.previousHeight - this.pos.y;
          this.previousHeight = this.pos.y;

          // the player died
          if (this.pos.y > lostLiveLevel) {
            kaplayContext.play(SOUND.hit);
            this.respawnPlayer();
          }

          if (
            !this.isMoving &&
            this.isGrounded() &&
            this.getCurAnim()?.name !== PLAYER_ANIMATION.idle
          ) {
            this.play(PLAYER_ANIMATION.idle);
          }

          if (!this.isGrounded()) {
            /*
             * Only play the animation, if it is not currently playing,
             * otherwise the Kaplay would start playing it from the first frame
             */
            if (
              this.heightDelta > 0 &&
              this.getCurAnim()?.name !== PLAYER_ANIMATION.jumpUp
            ) {
              this.play(PLAYER_ANIMATION.jumpUp);
            }

            if (
              this.heightDelta < 0 &&
              this.getCurAnim()?.name !== PLAYER_ANIMATION.jumpDown
            ) {
              this.play(PLAYER_ANIMATION.jumpDown);
            }
          }
        });
      },
    },
  ]);

  playerObject.setControls();
  playerObject.enablePassthrough();
  playerObject.enableCoinPickup();
  playerObject.enableCreatureAndItemVulnerability();
  playerObject.update();

  return playerObject;
};
