import {
  BACKGROUND_SPRITE_ID,
  BEST_SCORE_DATA,
  COLOR,
  CURSOR_SPRITE_ID,
  DUCK_COUNT_IN_ROUND,
  DUCK_ESCAPED_GAME_STATE_ID,
  DUCK_HUNTED_GAME_STATE_ID,
  DUCK_ICON_TAG_ID,
  FONT_CONFIG,
  GAME_OVER_SCENE_ID,
  GUN_SHOT_SOUND_ID,
  HUNT_END_GAME_STATE_ID,
  HUNT_START_GAME_STATE_ID,
  MAX_HUNT_NUMBER,
  ROUND_END_GAME_STATE_ID,
  ROUND_START_GAME_STATE_ID,
  SKY_TAG_ID,
  TEXT_BOX_SPRITE_ID,
  UI_APPEAR_SOUND_ID,
} from "../constants";
import createDog from "../entities/dog";
import createDuck from "../entities/duck";
import gameStateManager from "../game-state-manager";
import kaplayContext from "../kaplay-context";

export const game = () => {
  kaplayContext.setCursor("none");
  kaplayContext.add([
    kaplayContext.rect(kaplayContext.width(), kaplayContext.height()),
    kaplayContext.color(COLOR.BLUE),
    SKY_TAG_ID,
  ]);
  kaplayContext.add([
    kaplayContext.sprite(BACKGROUND_SPRITE_ID),
    kaplayContext.pos(0, -10),
    kaplayContext.z(1),
  ]);

  const score = kaplayContext.add([
    kaplayContext.text("0".toString().padStart(6, "0"), FONT_CONFIG),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.pos(192, 196),
  ]);

  const roundCounter = kaplayContext.add([
    kaplayContext.text("1", FONT_CONFIG),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.pos(42, 181),
    kaplayContext.color(COLOR.RED),
  ]);

  const duckIcons = kaplayContext.add([kaplayContext.pos(95, 198)]);
  let duckIconPositionX = 1;

  for (let index = 0; index < 10; index++) {
    duckIcons.add([
      kaplayContext.rect(7, 9),
      kaplayContext.pos(duckIconPositionX, 0),
      `${DUCK_ICON_TAG_ID}-${index}`,
    ]);
    duckIconPositionX += 8;
  }

  const bulletsUIMask = kaplayContext.add([
    kaplayContext.rect(0, 8),
    kaplayContext.pos(25, 198),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.color(COLOR.BLACK),
  ]);

  const cursor = kaplayContext.add([
    kaplayContext.sprite(CURSOR_SPRITE_ID),
    kaplayContext.anchor("center"),
    // we deliberately won't specify the position of the cursor,
    // because we want to use the method "moveTo()" which is available only if no arguments are passed
    kaplayContext.pos(),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(3),
  ]);

  const dog = createDog(kaplayContext.vec2(0, kaplayContext.center().y));
  dog.searchForDucks();

  // the method "onStateEnter()" is available on the game object,
  // because we used the component "state()" on it during the creation of the object
  const roundStartController = gameStateManager.onStateEnter(
    ROUND_START_GAME_STATE_ID,
    async (isFirstRound: boolean) => {
      if (!isFirstRound) {
        gameStateManager.duckSpeed += 50;
      }

      kaplayContext.play(UI_APPEAR_SOUND_ID);
      gameStateManager.currentRoundNumber++;
      roundCounter.text = gameStateManager.currentRoundNumber.toString();

      const textBox = kaplayContext.add([
        kaplayContext.sprite(TEXT_BOX_SPRITE_ID),
        kaplayContext.anchor("center"),
        kaplayContext.pos(
          kaplayContext.center().x,
          kaplayContext.center().y - 50,
        ),
        kaplayContext.z(2),
      ]);
      textBox.add([
        kaplayContext.text("ROUND", FONT_CONFIG),
        kaplayContext.anchor("center"),
        // the position of a child is relative to the position of its parent
        kaplayContext.pos(0, -10),
      ]);
      textBox.add([
        kaplayContext.text(
          gameStateManager.currentRoundNumber.toString(),
          FONT_CONFIG,
        ),
        kaplayContext.anchor("center"),
        // the position of a child is relative to the position of its parent
        kaplayContext.pos(0, 4),
      ]);

      // wait 1 second before next round starts
      await kaplayContext.wait(1);
      kaplayContext.destroy(textBox);
      gameStateManager.enterState(HUNT_START_GAME_STATE_ID);
    },
  );

  const roundEndController = gameStateManager.onStateEnter(
    ROUND_END_GAME_STATE_ID,
    () => {
      if (gameStateManager.numberOfDucksShotInRound < 6) {
        kaplayContext.go(GAME_OVER_SCENE_ID);
        return;
      }

      // player gets a bonus if all ducks were shot
      if (gameStateManager.numberOfDucksShotInRound === DUCK_COUNT_IN_ROUND) {
        gameStateManager.currentScore += 500;
      }

      gameStateManager.numberOfDucksShotInRound = 0;
      // restart the colour of each duck items to white
      for (const icon of duckIcons.children) {
        icon.color = kaplayContext.Color.fromHex(COLOR.WHITE);
      }

      gameStateManager.enterState(ROUND_START_GAME_STATE_ID);
    },
  );

  const huntStartController = gameStateManager.onStateEnter(
    HUNT_START_GAME_STATE_ID,
    () => {
      gameStateManager.currentHuntNumber++;
      const duck = createDuck({
        duckId: `${gameStateManager.currentHuntNumber - 1}`,
        speed: gameStateManager.duckSpeed,
      });
      duck.setBehaviour();
    },
  );

  const huntEndController = gameStateManager.onStateEnter(
    HUNT_END_GAME_STATE_ID,
    () => {
      const bestScore = kaplayContext.getData(BEST_SCORE_DATA) as number;

      if (bestScore < gameStateManager.currentScore) {
        kaplayContext.setData(BEST_SCORE_DATA, gameStateManager.currentScore);
      }

      if (gameStateManager.currentHuntNumber < MAX_HUNT_NUMBER) {
        gameStateManager.enterState(HUNT_START_GAME_STATE_ID);
        return;
      }

      gameStateManager.currentHuntNumber = 1;
      gameStateManager.enterState(ROUND_END_GAME_STATE_ID);
    },
  );

  const duckHuntedController = gameStateManager.onStateEnter(
    DUCK_HUNTED_GAME_STATE_ID,
    () => {
      gameStateManager.numberOfBulletsLeft = 3;
      dog.catchFallenDuck();
    },
  );

  const duckEscapedController = gameStateManager.onStateEnter(
    DUCK_ESCAPED_GAME_STATE_ID,
    () => {
      dog.laugtAtPlayer();
    },
  );

  kaplayContext.onClick(() => {
    // the property "state" is available on the game object,
    // because we used the component "state()" on it during the creation of the object
    if (
      gameStateManager.state === HUNT_START_GAME_STATE_ID &&
      !gameStateManager.isGamePaused
    ) {
      if (gameStateManager.numberOfBulletsLeft > 0) {
        kaplayContext.play(GUN_SHOT_SOUND_ID, { volume: 0.5 });
        gameStateManager.numberOfBulletsLeft--;
      }
    }
  });

  kaplayContext.onUpdate(() => {
    score.text = gameStateManager.currentScore.toString().padStart(6, "0");

    switch (gameStateManager.numberOfBulletsLeft) {
      case 3:
        bulletsUIMask.width = 0;
        break;
      case 2:
        bulletsUIMask.width = 8;
        break;
      case 1:
        bulletsUIMask.width = 15;
        break;
      default:
        bulletsUIMask.width = 22;
    }

    // move the cursor to the position of the mouse cursor
    cursor.moveTo(kaplayContext.mousePos());
  });

  kaplayContext.onSceneLeave(() => {
    roundStartController.cancel();
    roundEndController.cancel();
    huntStartController.cancel();
    huntEndController.cancel();
    duckHuntedController.cancel();
    duckEscapedController.cancel();
    gameStateManager.resetGameState();
  });
};
