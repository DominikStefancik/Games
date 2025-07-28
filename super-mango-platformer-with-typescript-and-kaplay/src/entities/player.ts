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
  const { playerStartPosition, playerSpeed, jumpForce } = levelConfig;

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
      setControls() {
        kaplayContext.onKeyDown(KEY_CONTROL.left, () => {
          if (playerObject.getCurAnim()?.name !== PLAYER_ANIMATION.run) {
            playerObject.play(PLAYER_ANIMATION.run);
          }
          playerObject.flipX = true;
          // the "move()" method is from Kaplay and it moves a game object in a vertical and horizontal direction
          playerObject.move(-playerSpeed, 0);
        });

        kaplayContext.onKeyDown(KEY_CONTROL.right, () => {
          if (playerObject.getCurAnim()?.name !== PLAYER_ANIMATION.run) {
            playerObject.play(PLAYER_ANIMATION.run);
          }
          playerObject.flipX = false;
          // the "move()" method is from Kaplay and it moves a game object in a vertical and horizontal direction
          playerObject.move(playerSpeed, 0);
        });

        kaplayContext.onKeyDown(KEY_CONTROL.space, () => {
          // the "isGrounded()" method is from Kaplay and it checks if a game object is on a platform
          if (playerObject.isGrounded()) {
            // the "jump()" method is from Kaplay and it jumps a game object in a vertical and horizontal direction
            playerObject.jump(jumpForce);
            kaplayContext.play(SOUND.jump);
          }
        });

        kaplayContext.onKeyRelease(
          [KEY_CONTROL.left, KEY_CONTROL.right],
          () => {
            playerObject.play(PLAYER_ANIMATION.idle);
          },
        );
      },
    },
  ]);

  playerObject.setControls();

  return playerObject;
};
