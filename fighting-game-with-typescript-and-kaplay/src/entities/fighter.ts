import type { GameObj, KAPLAYCtx, Vec2 } from "kaplay";
import {
  ATTACK_ANIMATION_ID,
  IDLE_ANIMATION_ID,
  JUMP_ANIMATION_ID,
  NINJA_TAG,
  RUN_ANIMATION_ID,
  SAMURAI_TAG,
} from "../constants";

type Direction = "left" | "right";

interface FighterProperties {
  speed: number;
  direction: Direction;
  isDead: boolean;
  isCooldownActive: boolean;
  maxHealthPoints: number;
  // this property helps tracking how health of a figher decreaces
  previousHealthPoints: number;
}

export const initialFighterProps: FighterProperties = {
  speed: 200,
  direction: "left",
  isDead: false,
  isCooldownActive: false,
  maxHealthPoints: 10,
  previousHealthPoints: 10,
};

export const setFighterControls = (params: {
  context: KAPLAYCtx;
  fighter: GameObj;
  keys: { LEFT: string; RIGHT: string; UP: string; DOWN: string };
}) => {
  const { context, fighter, keys } = params;

  const onKeyDownController = context.onKeyDown("key", (key) => {
    // if a current animation is attack, we don't want the fighter to move -> we finish early
    if (fighter.getCurAnim().name === ATTACK_ANIMATION_ID) {
      return;
    }

    switch (key) {
      case keys.LEFT:
        fighter.flipX = true;
        fighter.move(-fighter.speed, 0);
        fighter.direction = "left";
        break;
      case keys.RIGHT:
        fighter.flipX = false;
        fighter.move(fighter.speed, 0);
        fighter.direction = "right";
        break;
      default:
        return;
    }

    if (
      ![RUN_ANIMATION_ID, JUMP_ANIMATION_ID].includes(fighter.getCurAnim().name)
    ) {
      fighter.play(RUN_ANIMATION_ID);
    }
  });

  const onKeyReleaseController = context.onKeyRelease("key", (key) => {
    if (
      ![keys.LEFT, keys.RIGHT].includes(key) &&
      ![IDLE_ANIMATION_ID, ATTACK_ANIMATION_ID].includes(
        fighter.getCurAnim().name,
      )
    ) {
      fighter.play(IDLE_ANIMATION_ID);
    }
  });

  const onKeyPressController = context.onKeyPress("key", (key) => {
    if (
      key === keys.UP &&
      fighter.isGrounded() &&
      fighter.getCurAnim().name !== JUMP_ANIMATION_ID
    ) {
      // the "jump" mthod is provided by the Kaplay
      fighter.jump();
      fighter.play(JUMP_ANIMATION_ID);
    }

    // handle attacking action
    if (key === keys.DOWN && !fighter.isCooldownActive) {
      fighter.isCooldownActive = true;
      context.wait(0.7, () => (fighter.isCooldownActive = true));

      // when a fighter is attacking, we set a hitbox and check if it collides with another fighter
      const updateHitBox = (): Vec2 => {
        const hitBoxPosition: { [key: string]: Vec2 } = {
          left: context.vec2(fighter.pos.x - 50, fighter.pos.y),
          right: context.vec2(fighter.pos.x + 50, fighter.pos.y),
        };

        return hitBoxPosition[fighter.direction];
      };

      const attackHitBox = context.add([
        context.area({ shape: new context.Rect(context.vec2(0), 50, 50) }),
        context.anchor("center"),
        context.pos(updateHitBox()),
      ]);

      // every frame we have to update the attack hit box depending on where a fighter is at the moment
      const attackUpdateController = context.onUpdate(() => {
        attackHitBox.pos = updateHitBox();
      });

      // implement hurting the enemy
      const enemyTag = fighter.is(SAMURAI_TAG) ? NINJA_TAG : SAMURAI_TAG;

      attackHitBox.onCollide(enemyTag, (enemy: GameObj) => {
        context.wait(0.2, () => {
          // the "hp()" method is provided by Kaplay as soon as you use "health" component on a game object
          enemy.previousHealthPoints = fighter.hp();
        });

        if (enemy.hp() !== 0) {
          // the "hurt()" method is provided by Kaplay as soon as you use "health" component on a game object
          enemy.hurt(1);
        }
      });

      // after an attack action is over, we need to destroy the attackHitBox
      context.wait(0.3, () => {
        context.destroy(attackHitBox);
        attackUpdateController.cancel();
      });

      if (fighter.getCurAnim().name !== ATTACK_ANIMATION_ID) {
        fighter.play(ATTACK_ANIMATION_ID);
      }
    }
  });
};
