import {
  BUTTON_JUMP,
  GAME_SCENE_ID,
  INSTRUCTIONS_FONT_SIZE,
  LOCAL_STORAGE_BEST_SCORE_KEY,
  LOCAL_STORAGE_CURRENT_SCORE_KEY,
  MANIA_FONT_ID,
  SCORE_STATS_TEXT_FONT_SIZE,
  SCORE_STATS_VALUE_FONT_SIZE,
  TITLE_FONT_SIZE,
} from "../constants";
import kaplayContext from "../kaplay-context";

const gameOver = (citySoundEffect) => {
  citySoundEffect.paused = true;
  let bestScore = kaplayContext.getData(LOCAL_STORAGE_BEST_SCORE_KEY);
  let currentScore = kaplayContext.getData(LOCAL_STORAGE_CURRENT_SCORE_KEY);

  const rankGrades = ["F", "E", "D", "C", "B", "A", "S"];
  const rankValues = [50, 80, 100, 200, 300, 400, 500];

  let currentRank = "F";
  let bestRank = "F";

  for (let index = 0; index < rankValues.length; index++) {
    if (currentScore > rankValues[index]) {
      currentRank = rankGrades[index];
    }

    if (bestScore > rankValues[index]) {
      bestRank = rankGrades[index];
    }
  }

  if (currentScore > bestScore) {
    kaplayContext.setData(LOCAL_STORAGE_BEST_SCORE_KEY, currentScore);
    bestScore = currentScore;
    bestRank = currentRank;
  }

  kaplayContext.add([
    kaplayContext.text("GAME OVER", {
      font: MANIA_FONT_ID,
      size: TITLE_FONT_SIZE,
    }),
    // "center" method returns the center of the canvas
    kaplayContext.pos(kaplayContext.center().x, kaplayContext.center().y - 300),
    kaplayContext.anchor("center"),
  ]);

  kaplayContext.add([
    kaplayContext.text(`BEST SCORE: ${bestScore}`, {
      font: MANIA_FONT_ID,
      size: SCORE_STATS_TEXT_FONT_SIZE,
    }),
    // "center" method returns the center of the canvas
    kaplayContext.pos(
      kaplayContext.center().x - 400,
      kaplayContext.center().y - 200,
    ),
    kaplayContext.anchor("center"),
  ]);

  kaplayContext.add([
    kaplayContext.text(`CURRENT SCORE: ${currentScore}`, {
      font: MANIA_FONT_ID,
      size: SCORE_STATS_TEXT_FONT_SIZE,
    }),
    // "center" method returns the center of the canvas
    kaplayContext.pos(
      kaplayContext.center().x + 400,
      kaplayContext.center().y - 200,
    ),
    kaplayContext.anchor("center"),
  ]);

  const bestRankBox = kaplayContext.add([
    // "radius" option sets how round the corners will be
    kaplayContext.rect(400, 400, { radius: 4 }),
    kaplayContext.color(0, 0, 0),
    kaplayContext.area(),
    kaplayContext.anchor("center"),
    kaplayContext.pos(
      kaplayContext.center().x - 400,
      kaplayContext.center().y + 50,
    ),
    kaplayContext.outline(6, kaplayContext.Color.fromArray([255, 255, 255])),
  ]);

  bestRankBox.add([
    kaplayContext.text(bestRank, {
      font: MANIA_FONT_ID,
      size: SCORE_STATS_VALUE_FONT_SIZE,
    }),
    kaplayContext.anchor("center"),
  ]);

  const currentRankBox = kaplayContext.add([
    // "radius" option sets how round the corners will be
    kaplayContext.rect(400, 400, { radius: 4 }),
    kaplayContext.color(0, 0, 0),
    kaplayContext.area(),
    kaplayContext.anchor("center"),
    kaplayContext.pos(
      kaplayContext.center().x + 400,
      kaplayContext.center().y + 50,
    ),
    kaplayContext.outline(6, kaplayContext.Color.fromArray([255, 255, 255])),
  ]);

  currentRankBox.add([
    kaplayContext.text(bestRank, {
      font: MANIA_FONT_ID,
      size: SCORE_STATS_VALUE_FONT_SIZE,
    }),
    kaplayContext.anchor("center"),
  ]);

  kaplayContext.wait(1, () => {
    kaplayContext.add([
      kaplayContext.text("Press Space/Click/Touch to Play", {
        font: MANIA_FONT_ID,
        size: INSTRUCTIONS_FONT_SIZE,
      }),
      // "center" method returns the center of the canvas
      kaplayContext.pos(
        kaplayContext.center().x,
        kaplayContext.center().y + 350,
      ),
      kaplayContext.anchor("center"),
    ]);

    kaplayContext.onButtonPress(BUTTON_JUMP, () =>
      kaplayContext.go(GAME_SCENE_ID),
    );
  });
};

export default gameOver;
