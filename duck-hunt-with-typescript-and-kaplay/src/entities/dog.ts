import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import {
  DOG_STATE,
  GAME_STATE,
  DOG_ANIMATION,
  SPRITE,
  SOUND,
} from "../constants";
import gameStateManager from "../game-state-manager";

const createDog = (position: Vec2): GameObj => {
  const sniffingSound = kaplayContext.play(SOUND.sniffing, { volume: 2 });
  /*
   * We play the sound and immediatelly stop it.
   * That way we will have the sound available in the "sniffingSound" constant, so later we can play it again
   * Note: For a player, they will not hear anything, but we can play the sound later
   */
  sniffingSound.stop();

  const barkingSound = kaplayContext.play(SOUND.barking);
  barkingSound.stop();

  const laughingSound = kaplayContext.play(SOUND.laughing);
  laughingSound.stop();

  return kaplayContext.add([
    kaplayContext.sprite(SPRITE.dog),
    kaplayContext.pos(position),
    // defines a state machine specifically for the dog game object
    kaplayContext.state(DOG_STATE.search, [
      DOG_STATE.search,
      DOG_STATE.snif,
      DOG_STATE.detect,
      DOG_STATE.jump,
      DOG_STATE.drop,
    ]),
    kaplayContext.z(2),
    // custom properties
    {
      speed: 15,
      searchForDucks(this: GameObj) {
        let numberOfSnifs = 0;

        this.onStateEnter(DOG_STATE.search, () => {
          this.play(DOG_ANIMATION.searching);

          kaplayContext.wait(2, () => {
            this.enterState(DOG_STATE.snif);
          });
        });

        // defines what happens on every frame while the dog is searching
        this.onStateUpdate(DOG_STATE.search, () => {
          /*
           * The first argument: rate of a movement on the x-axis
           * The second argument: rate of a movement on the y-axis
           *
           * With the second argument being 0, the dog will move only horizontally
           */
          this.move(this.speed, 0);
        });

        this.onStateEnter(DOG_STATE.snif, () => {
          numberOfSnifs++;
          this.play(DOG_ANIMATION.sniffing);
          sniffingSound.play();
          kaplayContext.wait(2, () => {
            sniffingSound.stop();

            if (numberOfSnifs === 2) {
              this.enterState(DOG_STATE.detect);
              return;
            }

            this.enterState(DOG_STATE.search);
          });
        });

        this.onStateEnter(DOG_STATE.detect, () => {
          barkingSound.play();
          this.play(DOG_ANIMATION.detecting);

          kaplayContext.wait(1, () => {
            barkingSound.stop();
            this.enterState(DOG_STATE.jump);
          });
        });

        this.onStateEnter(DOG_STATE.jump, () => {
          barkingSound.play();
          this.play(DOG_ANIMATION.jumping);

          kaplayContext.wait(0.5, () => {
            barkingSound.stop();
            /*
             * The "use()" method is used after a game object has been created and we want to update one of its component.
             *
             * We change the z-value of the dog game object, so it looks like it is hidden behind the grass.
             */
            this.use(kaplayContext.z(0));
            this.enterState(DOG_STATE.drop);
          });
        });

        this.onStateUpdate(DOG_STATE.jump, () => {
          this.move(100, -50);
        });

        this.onStateEnter(DOG_STATE.drop, async () => {
          await kaplayContext.tween(
            this.pos.y,
            125,
            0.5,
            (newY) => (this.pos.y = newY),
            kaplayContext.easings.linear,
          );
          // the second argument represents the value for the "isFirstRound" argument,
          // see the "roundStartController" in the "game" function
          gameStateManager.enterState(GAME_STATE.roundStart, true);
        });
      },
      async showUpAndHide(this: GameObj) {
        // show the dog up
        await kaplayContext.tween(
          this.pos.y,
          90,
          0.4,
          (newY) => (this.pos.y = newY),
          kaplayContext.easings.linear,
        );
        // wait for 1 second
        await kaplayContext.wait(1);
        // and then hide the dog down
        await kaplayContext.tween(
          this.pos.y,
          125,
          0.4,
          (newY) => (this.pos.y = newY),
          kaplayContext.easings.linear,
        );
      },
      async catchFallenDuck(this: GameObj) {
        /*
         * When the method "play()" is called on a game object, it plays its animation
         * which name is passed as an argument.
         * When the method "play()" is called on the Kaplay's context object, it plays a sound
         * which name is passed as an argument.
         */
        this.play(DOG_ANIMATION.catching);
        kaplayContext.play(SOUND.successfulHunt);
        await this.showUpAndHide();
        gameStateManager.enterState(GAME_STATE.huntEnd);
      },
      async laugtAtPlayer(this: GameObj) {
        laughingSound.play();
        this.play(DOG_ANIMATION.laughing);
        await this.showUpAndHide();
        gameStateManager.enterState(GAME_STATE.huntEnd);
      },
    },
  ]);
};

export default createDog;
