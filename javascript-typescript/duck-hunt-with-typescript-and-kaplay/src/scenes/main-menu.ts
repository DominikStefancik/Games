import {
  BEST_SCORE_DATA,
  COLOR,
  FONT_CONFIG,
  SCENE,
  SPRITE,
} from "../constants";
import kaplayContext from "../kaplay-context";

export const mainMenu = () => {
  kaplayContext.add([kaplayContext.sprite(SPRITE.menu)]);
  kaplayContext.add([
    kaplayContext.text("CLICK TO START", FONT_CONFIG),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.anchor("center"),
    kaplayContext.pos(kaplayContext.center().x, kaplayContext.center().y + 40),
  ]);

  kaplayContext.add([
    kaplayContext.text("MADE BY DOMINIK STEFANCIK", FONT_CONFIG),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.pos(10, 205),
    kaplayContext.color(COLOR.BLUE),
    kaplayContext.opacity(0.5),
  ]);

  const bestScore: number = kaplayContext.getData(BEST_SCORE_DATA, 0)!;
  kaplayContext.add([
    kaplayContext.text(
      `TOP SCORE: ${bestScore.toString().padStart(6, "0")}`,
      FONT_CONFIG,
    ),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.pos(55, 184),
    kaplayContext.color(COLOR.RED),
    kaplayContext.opacity(0.5),
  ]);

  kaplayContext.onClick(() => {
    kaplayContext.go(SCENE.game);
  });
};
