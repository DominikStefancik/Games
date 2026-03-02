import type { GameObj } from "kaplay";
import { GAME_STATE } from "./constants";
import kaplayContext from "./kaplay-context";

const createGameStateManager = () => {
  return kaplayContext.add([
    /*
     * the method "state()" creates a finite state machine
     *
     * for each of the states we can define a custom logic which will be executed
     * when th game is in that state
     */
    kaplayContext.state(GAME_STATE.menu, [
      GAME_STATE.menu,
      GAME_STATE.roundStart,
      GAME_STATE.roundEnd,
      GAME_STATE.huntStart,
      GAME_STATE.huntEnd,
      GAME_STATE.duckHunted,
      GAME_STATE.duckEscaped,
    ]),
    // custom properties of the game object
    {
      isGamePaused: false,
      currentScore: 0,
      currentRoundNumber: 0,
      currentHuntNumber: 0,
      numberOfBulletsLeft: 3,
      numberOfDucksShotInRound: 0,
      duckSpeed: 100,
      resetGameState(this: GameObj) {
        this.isGamePaused = false;
        this.currentScore = 0;
        this.currentRoundNumber = 0;
        this.currentHuntNumber = 0;
        this.numberOfBulletsLeft = 3;
        this.numberOfDucksShotInRound = 0;
        this.duckSpeed = 100;
      },
    },
  ]);
};

// this will ensure that a game manager object is only created once
// and the same object exported as many times as needed
const gameStateManager = createGameStateManager();

export default gameStateManager;
