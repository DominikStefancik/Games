import type { GameObj, KAPLAYCtx, Vec2 } from "kaplay";
import {
  ARENA_SCENE,
  ATTACK_ANIMATION_ID,
  DYING_ANIMATION_ID,
  FALL_ANIMATION_ID,
  HIT_ANIMATION_ID,
  HURT_EVENT_ID,
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

const makeFighterBlink = async (params: {
  context: KAPLAYCtx;
  fighter: GameObj;
}) => {
  const { context, fighter } = params;

  // tweening is gradually changing one value to another by using an easing function
  await context.tween(
    fighter.opacity, // initial value
    0, // final value
    0.5, // duration how long it would take to change the initial value to the final one
    (newOpacity) => (fighter.opacity = newOpacity), // function describing how value should change
    context.easings.linear,
  );
  await context.tween(
    fighter.opacity, // after the first tween, the opacity is 0
    1, // we want to bring the opacity back to 1
    0.5,
    (newOpacity) => (fighter.opacity = newOpacity),
    context.easings.linear,
  );
};

export const setFighterControls = (params: {
  context: KAPLAYCtx;
  fighter: GameObj;
  keys: { LEFT: string; RIGHT: string; UP: string; DOWN: string };
}) => {
  const { context, fighter, keys } = params;

  const onKeyDownController = context.onKeyDown((key) => {
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

  const onKeyReleaseController = context.onKeyRelease((key) => {
    if (
      [keys.LEFT, keys.RIGHT].includes(key) &&
      ![IDLE_ANIMATION_ID, ATTACK_ANIMATION_ID].includes(
        fighter.getCurAnim().name,
      )
    ) {
      fighter.play(IDLE_ANIMATION_ID);
    }
  });

  const onKeyPressController = context.onKeyPress((key) => {
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
      context.wait(0.7, () => (fighter.isCooldownActive = false));

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

      if (fighter.getCurAnim().name !== ATTACK_ANIMATION_ID) {
        fighter.play(ATTACK_ANIMATION_ID);
      }

      // after an attack action is over, we need to destroy the attackHitBox
      context.wait(0.3, () => {
        context.destroy(attackHitBox);
        attackUpdateController.cancel();
      });
    }
  });

  // when the Kaplay's method "hurt()" runs, it emits the "hurt" event
  fighter.on(HURT_EVENT_ID, async () => {
    await makeFighterBlink({ context, fighter });
    if (fighter.hp() > 0 && fighter.getCurAnim().name !== HIT_ANIMATION_ID) {
      fighter.play(HIT_ANIMATION_ID);
      return;
    }

    if (
      fighter.hp() === 0 &&
      fighter.getCurAnim().name !== DYING_ANIMATION_ID
    ) {
      fighter.isDead = true;

      // we need to unregister the event listeners, because a dead fighter should not react to events
      onKeyDownController.cancel();
      onKeyReleaseController.cancel();
      onKeyPressController.cancel();

      fighter.play(DYING_ANIMATION_ID);

      // show who won and who lost
      const enemyTag = fighter.is(SAMURAI_TAG) ? NINJA_TAG : SAMURAI_TAG;
      // the property "recursive" says that the Kaply will search for objects with the given tag
      // also among children of game objects
      const enemyObject = context.get(enemyTag, { recursive: true })[0];

      const enemyStatus = context.add([
        context.text("WINNER", { size: 16 }),
        context.area(),
        context.anchor("center"),
        context.pos(),
      ]);

      const fighterStatus = context.add([
        context.text("LOSER", { size: 16 }),
        context.area(),
        context.anchor("center"),
        context.pos(),
      ]);

      context.onUpdate(() => {
        enemyStatus.pos = context.vec2(
          enemyObject.pos.x,
          enemyObject.pos.y - 40,
        );

        // this is specifically for the ninja fighter
        // so the text aligns with the dead ninja body more closely
        if (fighter.is(NINJA_TAG) && fighter.isDead()) {
          fighterStatus.pos = context.vec2(
            fighter.pos.x - 25,
            fighter.pos.y - 5,
          );
          return;
        }

        fighterStatus.pos = context.vec2(fighter.pos.x, fighter.pos.y - 40);

        context.wait(5, () => context.go(ARENA_SCENE));
      });
    }
  });

  context.onUpdate(() => {
    // the "isJumping()" mthod is provided by the Kaplay and checks if a game object is not isGrounded
    // and is ascending at the same time
    if (
      !fighter.isJumping() &&
      !fighter.isGrounded() &&
      ![FALL_ANIMATION_ID, ATTACK_ANIMATION_ID].includes(
        fighter.getCurAnim().name,
      )
    ) {
      fighter.play(FALL_ANIMATION_ID);
    }

    console.log("Fighter: ", fighter);
    console.log("Current anim: ", fighter.getCurAnim());
    // a fighter was falling and reached out the ground
    if (
      fighter.getCurAnim().name === FALL_ANIMATION_ID &&
      fighter.isGrounded()
    ) {
      fighter.play(IDLE_ANIMATION_ID);
    }

    if (
      ![
        IDLE_ANIMATION_ID,
        JUMP_ANIMATION_ID,
        ATTACK_ANIMATION_ID,
        HIT_ANIMATION_ID,
        FALL_ANIMATION_ID,
        RUN_ANIMATION_ID,
      ].includes(fighter.getCurAnim().name) &&
      !fighter.isDead
    ) {
      fighter.play(IDLE_ANIMATION_ID);
    }
  });
};
