import {
  BEST_SCORE_DATA,
  COLOR,
  GAME_SCENE_ID,
  MENU_SPRITE_ID,
  NES_FONT_ID,
} from "../constants";
import kaplayContext from "../kaplay-context";

export const mainMenu = () => {
  kaplayContext.add([kaplayContext.sprite(MENU_SPRITE_ID)]);
  kaplayContext.add([
    kaplayContext.text("CLICK TO START", { font: NES_FONT_ID, size: 8 }),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.anchor("center"),
    kaplayContext.pos(kaplayContext.center().x, kaplayContext.center().y + 40),
  ]);

  kaplayContext.add([
    kaplayContext.text("MADE BY DOMINIK STEFANCIK", {
      font: NES_FONT_ID,
      size: 8,
    }),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    // kaplayContext.anchor("center"),
    kaplayContext.pos(10, 215),
    kaplayContext.color(COLOR.BLUE),
    kaplayContext.opacity(0.5),
  ]);

  const bestScore: number = kaplayContext.getData(BEST_SCORE_DATA, 0)!;
  kaplayContext.add([
    kaplayContext.text(`TOP SCORE: ${bestScore.toString().padStart(6, "0")}`, {
      font: NES_FONT_ID,
      size: 8,
    }),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.pos(55, 184),
    kaplayContext.color(COLOR.RED),
    kaplayContext.opacity(0.5),
  ]);

  kaplayContext.onClick(() => {
    kaplayContext.go(GAME_SCENE_ID);
  });
};
