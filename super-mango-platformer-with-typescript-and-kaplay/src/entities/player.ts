import type { GameObj } from "kaplay";
import kaplayContext from "../kaplay-context";
import {
  ENTITY_SPRITE,
  KEY_CONTROL,
  PLAYER_ANIMATION,
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
    // custom properties specific to a player playerObject
    {
      lives: playerLivesCount,
      isRespawning: false,
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
          }
        });

        kaplayContext.onKeyDown(KEY_CONTROL.space, () => {
          // the "isGrounded()" method is from Kaplay and it checks if a game object is on a platform
          if (this.isGrounded() && !this.isRespawning) {
            // the "jump()" method is from Kaplay and it jumps a game object in a vertical and horizontal direction
            this.jump(jumpForce);
            kaplayContext.play(SOUND.jump);
          }
        });

        kaplayContext.onKeyRelease(
          [KEY_CONTROL.left, KEY_CONTROL.right],
          () => {
            this.play(PLAYER_ANIMATION.idle);
          },
        );
      },

      respawnPlayer(this: GameObj) {
        if (this.lives > 0) {
          this.pos = playerStartPosition;
          this.isRespawning = true;
          kaplayContext.wait(1, () => (this.isRespawning = false));
        }
      },

      update(this: GameObj) {
        kaplayContext.onUpdate(() => {
          // the player died
          if (this.pos.y > lostLiveLevel) {
            kaplayContext.play(SOUND.hit);
            this.respawnPlayer();
          }
        });
      },
    },
  ]);

  playerObject.setControls();

  return playerObject;
};
