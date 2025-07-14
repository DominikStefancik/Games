import {
  BACKGROUND_SPRITE_ID,
  COLOR,
  DUCK_ICON_TAG_ID,
  NES_FONT_ID,
  SKY_TAG_ID,
} from "../constants";
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
  kaplayContext.add([
    kaplayContext.text("0".toString().padStart(6, "0"), {
      font: NES_FONT_ID,
      size: 8,
    }),
    // defines a "z-layer" which is used when we want to display game objects on top of each other
    kaplayContext.z(2),
    kaplayContext.pos(192, 196),
  ]);

  const roundCounter = kaplayContext.add([
    kaplayContext.text("1", {
      font: NES_FONT_ID,
      size: 8,
    }),
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
};
