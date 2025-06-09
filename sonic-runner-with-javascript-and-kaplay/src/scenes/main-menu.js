import {
  BUTTON_JUMP,
  GAME_SCENE_ID,
  INSTRUCTIONS_FONT_SIZE,
  LOCAL_STORAGE_BEST_SCORE_KEY,
  MANIA_FONT_ID,
  TITLE_FONT_SIZE,
} from "../constants";
import { createSonic } from "../entities/sonic";
import kaplayContext from "../kaplay-context";
import {
  createBackgroundPieces,
  createPlatformPieces,
  switchBackgroundPieces,
  switchPlatformPieces,
} from "./scene-helpers";

const mainMenu = () => {
  // kaplay checks in the local storage for the best score
  if (!kaplayContext.getData(LOCAL_STORAGE_BEST_SCORE_KEY)) {
    kaplayContext.setData(LOCAL_STORAGE_BEST_SCORE_KEY, 0);
  }

  // the "BUTTON_JUMP" button is defined in the kaplay context
  kaplayContext.onButtonPress(BUTTON_JUMP, () =>
    kaplayContext.go(GAME_SCENE_ID),
  );

  ////////////////////////////////////////////////////////
  // adding background image
  const backgroundPieces = createBackgroundPieces();

  ////////////////////////////////////////////////////////
  // adding platform image
  const platformsPieces = createPlatformPieces();

  ////////////////////////////////////////////////////////
  // adding text
  kaplayContext.add([
    kaplayContext.text("SONIC RING RUN", {
      font: MANIA_FONT_ID,
      size: TITLE_FONT_SIZE,
    }),
    // "center" method returns the center of the canvas
    kaplayContext.pos(kaplayContext.center().x, 200),
    kaplayContext.anchor("center"),
  ]);

  kaplayContext.add([
    kaplayContext.text("Press Space/Click/Touch to Play", {
      font: MANIA_FONT_ID,
      size: INSTRUCTIONS_FONT_SIZE,
    }),
    // "center" method returns the center of the canvas
    kaplayContext.pos(kaplayContext.center().x, kaplayContext.center().y - 200),
    kaplayContext.anchor("center"),
  ]);

  ////////////////////////////////////////////////////////
  // adding Sonic image
  createSonic(kaplayContext.vec2(200, 745));

  // "onUpdate" method will run the function passed as an argument for every frame (60 times per second)
  kaplayContext.onUpdate(() => {
    switchBackgroundPieces(backgroundPieces);
    switchPlatformPieces(platformsPieces, 2000);
  });
};

export default mainMenu;
