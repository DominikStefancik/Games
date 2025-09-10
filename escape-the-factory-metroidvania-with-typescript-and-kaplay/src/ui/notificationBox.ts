import type { GameObj } from "kaplay";
import kaplayContext from "../kaplay-context";
import { FONT } from "../constants";

export const createNotificationBox = (content: string): GameObj => {
  const container = kaplayContext.make([
    kaplayContext.rect(580, 100),
    kaplayContext.color(kaplayContext.Color.fromHex("#20214a")),
    kaplayContext.fixed(),
    kaplayContext.pos(kaplayContext.center()),
    kaplayContext.area(),
    kaplayContext.anchor("center"),
    {
      close(this: GameObj) {
        kaplayContext.destroy(this);
      },
    },
  ]);

  container.add([
    kaplayContext.text(content, { font: FONT.glyphmesss, size: 32 }),
    kaplayContext.color(kaplayContext.Color.fromHex("eacfba")),
    kaplayContext.area(),
    kaplayContext.anchor("center"),
  ]);

  return container;
};
