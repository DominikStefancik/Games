import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import {
  BARKING_SOUND_ID,
  CATCHING_ANIMATION_ID,
  DETECT_DOG_STATE_ID,
  DETECTING_ANIMATION_ID,
  DOG_SPRITE_ID,
  DROP_DOG_STATE_ID,
  HUNT_END_GAME_STATE_ID,
  JUMP_DOG_STATE_ID,
  JUMPING_ANIMATION_ID,
  LAUGHING_ANIMATION_ID,
  LAUGHING_SOUND_ID,
  ROUND_START_GAME_STATE_ID,
  SEARCH_DOG_STATE_ID,
  SEARCHING_ANIMATION_ID,
  SNIF_DOG_STATE_ID,
  SNIFFING_ANIMATION_ID,
  SNIFFING_SOUND_ID,
  SUCCESSFUL_HUNT_SOUND_ID,
} from "../constants";
import gameStateManager from "../game-state-manager";

const createDog = (position: Vec2): GameObj => {
  const sniffingSound = kaplayContext.play(SNIFFING_SOUND_ID, { volume: 2 });
  /*
   * We play the sound and immediatelly stop it.
   * That way we will have the sound available in the "sniffingSound" constant, so later we can play it again
   * Note: For a player, they will not hear anything, but we can play the sound later
   */
  sniffingSound.stop();

  const barkingSound = kaplayContext.play(BARKING_SOUND_ID);
  barkingSound.stop();

  const laughingSound = kaplayContext.play(LAUGHING_SOUND_ID);
  laughingSound.stop();

  return kaplayContext.add([
    kaplayContext.sprite(DOG_SPRITE_ID),
    kaplayContext.pos(position),
    // defines a state machine specifically for the dog game object
    kaplayContext.state(SEARCH_DOG_STATE_ID, [
      SEARCH_DOG_STATE_ID,
      SNIF_DOG_STATE_ID,
      DETECT_DOG_STATE_ID,
      JUMP_DOG_STATE_ID,
      DROP_DOG_STATE_ID,
    ]),
    kaplayContext.z(2),
    // custom properties
    {
      speed: 15,
      searchForDucks(this: GameObj) {
        let numberOfSnifs = 0;

        this.onStateEnter(SEARCH_DOG_STATE_ID, () => {
          this.play(SEARCHING_ANIMATION_ID);

          kaplayContext.wait(2, () => {
            this.enterState(SNIF_DOG_STATE_ID);
          });
        });

        // defines what happens on every frame while the dog is searching
        this.onStateUpdate(SEARCH_DOG_STATE_ID, () => {
          /*
           * The first argument: rate of a movement on the x-axis
           * The second argument: rate of a movement on the y-axis
           *
           * With the second argument being 0, the dog will move only horizontally
           */
          this.move(this.speed, 0);
        });

        this.onStateEnter(SNIF_DOG_STATE_ID, () => {
          numberOfSnifs++;
          this.play(SNIFFING_ANIMATION_ID);
          sniffingSound.play();
          kaplayContext.wait(2, () => {
            sniffingSound.stop();

            if (numberOfSnifs === 2) {
              this.enterState(DETECT_DOG_STATE_ID);
              return;
            }

            this.enterState(SEARCH_DOG_STATE_ID);
          });
        });

        this.onStateEnter(DETECT_DOG_STATE_ID, () => {
          barkingSound.play();
          this.play(DETECTING_ANIMATION_ID);

          kaplayContext.wait(1, () => {
            barkingSound.stop();
            this.enterState(JUMP_DOG_STATE_ID);
          });
        });

        this.onStateEnter(JUMP_DOG_STATE_ID, () => {
          barkingSound.play();
          this.play(JUMPING_ANIMATION_ID);

          kaplayContext.wait(0.5, () => {
            barkingSound.stop();
            /*
             * The "use()" method is used after a game object has been created and we want to update one of its component.
             *
             * We change the z-value of the dog game object, so it looks like it is hidden behind the grass.
             */
            this.use(kaplayContext.z(0));
            this.enterState(DROP_DOG_STATE_ID);
          });
        });

        this.onStateUpdate(JUMP_DOG_STATE_ID, () => {
          this.move(100, -50);
        });

        this.onStateEnter(DROP_DOG_STATE_ID, async () => {
          await kaplayContext.tween(
            this.pos.y,
            125,
            0.5,
            (newY) => (this.pos.y = newY),
            kaplayContext.easings.linear,
          );
          // the second argument represents the value for the "isFirstRound" argument,
          // see the "roundStartController" in the "game" function
          gameStateManager.enterState(ROUND_START_GAME_STATE_ID, true);
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
        this.play(CATCHING_ANIMATION_ID);
        kaplayContext.play(SUCCESSFUL_HUNT_SOUND_ID);
        await this.showUpAndHide();
        gameStateManager.enterState(HUNT_END_GAME_STATE_ID);
      },
      async laugtAtPlayer(this: GameObj) {
        laughingSound.play();
        this.play(LAUGHING_ANIMATION_ID);
        await this.showUpAndHide();
        gameStateManager.enterState(HUNT_END_GAME_STATE_ID);
      },
    },
  ]);
};

export default createDog;
