import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import {
  ANIMATION,
  CUSTOM_EVENT,
  ENTITY_SPRITE,
  ENTITY_STATE,
  KAPLAY_EVENT,
  OFFSCREEN_DISTANCE,
  SOUND,
  TAG,
} from "../constants";

export const createEnemyDrone = (initialPosition: Vec2): GameObj => {
  return kaplayContext.make([
    kaplayContext.sprite(ENTITY_SPRITE.drone, { anim: ANIMATION.drone.flying }),
    kaplayContext.pos(initialPosition),
    kaplayContext.area({
      shape: new kaplayContext.Rect(kaplayContext.vec2(0), 12, 12),
    }),
    // by setting the "gravityScale" to 0, a game object will not be affected by gravity at all
    kaplayContext.body({ gravityScale: 0 }),
    kaplayContext.anchor("center"),
    kaplayContext.offscreen({ distance: OFFSCREEN_DISTANCE }),
    kaplayContext.state(ENTITY_STATE.drone.patrolRight, [
      ENTITY_STATE.drone.patrolRight,
      ENTITY_STATE.drone.patrolLeft,
      ENTITY_STATE.drone.alert,
      ENTITY_STATE.drone.attack,
      ENTITY_STATE.drone.retreat,
    ]),
    kaplayContext.health(1),
    TAG.drone,
    {
      // the speed at which a drone patrols from lrft to right
      speed: 100,
      // the speed with which a drone follows the player
      pursuitSpeed: 150,
      // the range in which a drone sees the player and starts following him
      alertRange: 100,
      setBehaviour(this: GameObj) {
        // since the Player game object is a child of a map, which is another game object,
        // we have to set the flag "recursive" to find him
        const player = kaplayContext.get(TAG.player, { recursive: true })[0];

        setBehaviourForPatrolRightState(this, player);
        setBehaviourForPatrolLeftState(this, player);
        setBehaviourForAlertState(this, player);
        setBehaviourForAttacState(this, player);
      },
      setEvents(this: GameObj) {
        const player = kaplayContext.get(TAG.player, { recursive: true })[0];

        // the method "onCollide" from Kaplay when a drone collides with a game object which has a given tag
        this.onCollide(TAG.player, () => {
          if (player.isAttacking) {
            return;
          }

          // the method "hurt" from Kaplay is provided when a game object has the "health" component
          this.hurt(1);
          player.hurt(1);
        });

        this.onAnimEnd((animation: string) => {
          if (animation === ANIMATION.drone.explode) {
            kaplayContext.destroy(this);
          }
        });

        this.on(CUSTOM_EVENT.explode, () => {
          kaplayContext.play(SOUND.boom);
          // while a drone is exploding, it is still colliding with a player
          // therefore we want to prevent any reaction for subsequent collisions
          this.collisionIgnore = [TAG.player];
          // the method "unuse" from Kaplay says which game object's component we don't want to use anymore
          this.unuse("body");
          this.play(ANIMATION.drone.explode);
        });

        // the method "onCollide" from Kaplay when a drone collides with a game object which has a given tag
        this.onCollide(TAG["sword-hitbox"], () => {
          // if the player's sword hits a drone, it will only hurt the drone, not the player
          // the method "hurt" from Kaplay will trigger the "hurt" event
          this.hurt(1);
        });

        this.on(KAPLAY_EVENT.hurt, () => {
          // the method "hp" is from Kaplay
          if (this.hp() === 0) {
            this.trigger(CUSTOM_EVENT.explode);
          }
        });

        // the method "onExitScreen" from Kaplay ia available if a game object has the "offscreen" component
        this.onExitScreen(() => {
          // a  drone is not destryoed and gets out of the screen, swet its position to it initial place
          this.pos = initialPosition;
        });
      },
    },
  ]);
};

const setBehaviourForPatrolRightState = (drone: GameObj, player: GameObj) => {
  drone.onStateEnter(ENTITY_STATE.drone.patrolRight, async () => {
    await kaplayContext.wait(3);

    /*
     * because below we have defined an event handler for the "onStateUpdate" for the "patrolRight" state
     * and we first wait 3 seconds in this function, the drone state can change, before we get to the following
     * IF condition, so we need to check whether a drone is in the state "patrolRight"
     */
    if (drone.state === ENTITY_STATE.drone.patrolRight) {
      drone.enterState(ENTITY_STATE.drone.patrolLeft);
    }
  });

  // the method "onStateUpdate" will run on every frame update if a game object is in a given state
  drone.onStateUpdate(ENTITY_STATE.drone.patrolRight, () => {
    if (drone.pos.dist(player.pos) < drone.alertRange) {
      drone.enterState(ENTITY_STATE.drone.alert);
      return;
    }

    drone.flipX = false;
    drone.move(drone.speed, 0);
  });
};

const setBehaviourForPatrolLeftState = (drone: GameObj, player: GameObj) => {
  drone.onStateEnter(ENTITY_STATE.drone.patrolLeft, async () => {
    await kaplayContext.wait(3);

    /*
     * because below we have defined an event handler for the "onStateUpdate" for the "patrolLeft" state
     * and we first wait 3 seconds in this function, the drone state can change, before we get to the following
     * IF condition, so we need to check whether a drone is in the state "patrolLeft"
     */
    if (drone.state === ENTITY_STATE.drone.patrolLeft) {
      drone.enterState(ENTITY_STATE.drone.patrolRight);
    }
  });

  // the method "onStateUpdate" will run on every frame update if a game object is in a given state
  drone.onStateUpdate(ENTITY_STATE.drone.patrolLeft, () => {
    if (drone.pos.dist(player.pos) < drone.alertRange) {
      drone.enterState(ENTITY_STATE.drone.alert);
      return;
    }

    drone.flipX = true;
    drone.move(-drone.speed, 0);
  });
};

const setBehaviourForAlertState = (drone: GameObj, player: GameObj) => {
  drone.onStateEnter(ENTITY_STATE.drone.alert, async () => {
    await kaplayContext.wait(1);

    if (drone.pos.dist(player.pos) < drone.alertRange) {
      drone.enterState(ENTITY_STATE.drone.attack);
      return;
    }

    drone.enterState(ENTITY_STATE.drone.patrolRight);
  });
};

const setBehaviourForAttacState = (drone: GameObj, player: GameObj) => {
  // the method "onStateUpdate" will run on every frame update if a game object is in a given state
  drone.onStateUpdate(ENTITY_STATE.drone.attack, () => {
    if (drone.pos.dist(player.pos) > drone.alertRange) {
      drone.enterState(ENTITY_STATE.drone.alert);
      return;
    }

    drone.flipX = player.pos.x <= drone.pos.x;
    drone.moveTo(
      kaplayContext.vec2(player.pos.x, player.pos.y + 12),
      drone.pursuitSpeed,
    );
  });
};
