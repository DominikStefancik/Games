import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import {
  ANIMATION,
  CUSTOM_EVENT,
  ENTITY_SPRITE,
  ENTITY_STATE,
  KAPLAY_EVENT,
  SOUND,
  TAG,
} from "../constants";
import { stateManager } from "../state/globalStateManager";
import { createNotificationBox } from "../ui/notificationBox";
import { makeEntityBlink } from "./helpers";

export const createEnemyBoss = (initialPosition: Vec2): GameObj => {
  return kaplayContext.make([
    kaplayContext.sprite(ENTITY_SPRITE.bossBurner, {
      anim: ANIMATION.bossBurner.idle,
    }),
    kaplayContext.pos(initialPosition),
    kaplayContext.area({
      shape: new kaplayContext.Rect(kaplayContext.vec2(0, 10), 12, 12),
    }),
    kaplayContext.body({ mass: 100 }),
    kaplayContext.anchor("center"),
    kaplayContext.state(ENTITY_STATE.bossBurner.idle, [
      ENTITY_STATE.bossBurner.idle,
      ENTITY_STATE.bossBurner.follow,
      ENTITY_STATE.bossBurner.openFire,
      ENTITY_STATE.bossBurner.fire,
      ENTITY_STATE.bossBurner.shutFire,
      ENTITY_STATE.bossBurner.explode,
    ]),
    kaplayContext.health(15),
    kaplayContext.opacity(1),
    {
      pursuitSpeed: 100,
      fireRange: 40,
      fireDuration: 1,
      setBehaviour(this: GameObj) {
        const player = kaplayContext.get(TAG.player, { recursive: true })[0];

        setBehaviourForIdleState(this);
        setBehaviourForFollowState(this, player);
        setBehaviourForOpenFireState(this);
        setBehaviourForFireState(this, player);
        setBehaviourForShutFireState(this);
      },
      setEvents(this: GameObj) {
        const player = kaplayContext.get(TAG.player, { recursive: true })[0];

        this.onCollide(TAG["sword-hitbox"], () => {
          kaplayContext.play(SOUND.boom);
          this.hurt(1);
        });

        this.onAnimEnd((animation: string) => {
          switch (animation) {
            case ANIMATION.bossBurner.openFire:
              this.enterState(ENTITY_STATE.bossBurner.fire);
              break;
            case ANIMATION.bossBurner.shutFire:
              this.enterState(ENTITY_STATE.bossBurner.follow);
              break;
            case ANIMATION.bossBurner.explode:
              kaplayContext.destroy(this);
              break;
            default:
              break;
          }
        });

        this.on(CUSTOM_EVENT.explode, () => {
          this.enterState(ENTITY_STATE.bossBurner.explode);
          kaplayContext.play(SOUND.boom);
          // while a boss is exploding, it is still colliding with a player
          // therefore we want to prevent any reaction for subsequent collisions
          this.collisionIgnore = [TAG.player];
          // the method "unuse" from Kaplay says which game object's component we don't want to use anymore
          this.unuse("body");
          this.play(ANIMATION.bossBurner.explode);
          stateManager.setState("isBossDefeated", true);
          stateManager.setState("isDoubleJumpUnlocked", true);
          player.enableDoubleJump();
          kaplayContext.play(SOUND.notify);
          const notification = kaplayContext.add(
            createNotificationBox(
              "You have unlocked a new ability!\nNow you can double jump",
            ),
          );
          kaplayContext.wait(3, () => {
            notification.close();
          });
        });

        this.on(KAPLAY_EVENT.hurt, () => {
          makeEntityBlink(this);

          if (this.hp() === 0) {
            this.trigger(CUSTOM_EVENT.explode);
          }
        });
      },
    },
  ]);
};

const setBehaviourForIdleState = (bossBurner: GameObj) => {
  // the method "onStateUpdate" will run on every frame update if a game object is in a given state
  bossBurner.onStateUpdate(ENTITY_STATE.bossBurner.idle, () => {
    if (stateManager.getState().isPlayerInFightWithBoss) {
      bossBurner.enterState(ENTITY_STATE.bossBurner.follow);
    }
  });
};

const setBehaviourForFollowState = (bossBurner: GameObj, player: GameObj) => {
  bossBurner.onStateEnter(ENTITY_STATE.bossBurner.follow, () => {
    bossBurner.play(ANIMATION.bossBurner.run);
  });

  bossBurner.onStateUpdate(ENTITY_STATE.bossBurner.follow, () => {
    bossBurner.flipX = player.pos.x <= bossBurner.pos.x;
    bossBurner.moveTo(
      kaplayContext.vec2(player.pos.x, player.pos.y),
      bossBurner.pursuitSpeed,
    );

    if (bossBurner.pos.dist(player.pos) <= bossBurner.fireRange) {
      bossBurner.enterState(ENTITY_STATE.bossBurner.openFire);
    }
  });
};

const setBehaviourForOpenFireState = (bossBurner: GameObj) => {
  bossBurner.onStateEnter(ENTITY_STATE.bossBurner.openFire, () => {
    bossBurner.play(ANIMATION.bossBurner.openFire);
  });
};

const setBehaviourForFireState = (bossBurner: GameObj, player: GameObj) => {
  bossBurner.onStateEnter(ENTITY_STATE.bossBurner.fire, () => {
    const flamethrowerSound = kaplayContext.play(SOUND.flamethrower);

    if (bossBurner.getCurAnim()?.name !== ANIMATION.bossBurner.fire) {
      bossBurner.play(ANIMATION.bossBurner.fire);
    }

    // when attacking, we create an invisible hitbox. If the player collides with this inbox,
    // he will receive damage
    const fireHitBox = bossBurner.add([
      kaplayContext.pos(bossBurner.flipX ? -70 : 0, 5),
      kaplayContext.area({
        shape: new kaplayContext.Rect(kaplayContext.vec2(0), 70, 10),
      }),
      TAG["fire-hitbox"],
    ]);

    fireHitBox.onCollide(TAG.player, async (player) => {
      player.hurt(1);

      if (player.hp() === 0) {
        flamethrowerSound.stop();
        // the player died, the boss fight is over
        stateManager.setState("isPlayerInFightWithBoss", false);
      }
    });

    kaplayContext.wait(bossBurner.fireDuration, () => {
      flamethrowerSound.stop();
      bossBurner.enterState(ENTITY_STATE.bossBurner.shutFire);
    });
  });

  bossBurner.onStateEnd(ENTITY_STATE.bossBurner.fire, () => {
    const fireHitBox = kaplayContext.get(TAG["fire-hitbox"], {
      recursive: true,
    })[0];

    if (fireHitBox) {
      kaplayContext.destroy(fireHitBox);
    }
  });
};

const setBehaviourForShutFireState = (bossBurner: GameObj) => {
  bossBurner.onStateEnter(ENTITY_STATE.bossBurner.shutFire, () => {
    bossBurner.play(ANIMATION.bossBurner.shutFire);
  });
};
