import { SCENE_ELEMENT_SPRITE, TAG, TILE_ANIMATION } from "../constants";
import kaplayContext from "../kaplay-context";

export type TileType = "grass";

// generates various mappings to various symbols in a map
export const generateMappings = (tileType: TileType) => {
  return {
    0: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.topLeft,
      }),
      kaplayContext.area(),
      // the property "isStatic" says that the game object will not be affected by gravity
      kaplayContext.body({ isStatic: true }),
      /*
       * the component "offscreen()" is used for performance reasons.
       * If a game object gets out of the screen, Kaplay stop calculations on this object
       */
      kaplayContext.offscreen(),
    ],
    1: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.topMiddle,
      }),
      kaplayContext.area(),
      kaplayContext.body({ isStatic: true }),
      kaplayContext.offscreen(),
    ],
    2: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.topRight,
      }),
      kaplayContext.area(),
      kaplayContext.body({ isStatic: true }),
      kaplayContext.offscreen(),
    ],
    3: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.middleLeft,
      }),
      kaplayContext.area(),
      kaplayContext.body({ isStatic: true }),
      kaplayContext.offscreen(),
    ],
    4: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.middleMiddle,
      }),
      kaplayContext.offscreen(),
    ],
    5: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.middleRight,
      }),
      kaplayContext.area(),
      kaplayContext.body({ isStatic: true }),
      kaplayContext.offscreen(),
    ],
    6: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.bottomLeft,
      }),
      kaplayContext.offscreen(),
    ],
    7: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.bottomMiddle,
      }),
      kaplayContext.offscreen(),
    ],
    8: () => [
      kaplayContext.sprite(`${tileType}Tileset`, {
        anim: TILE_ANIMATION.bottomRight,
      }),
      kaplayContext.offscreen(),
    ],
    9: () => [
      kaplayContext.sprite(`${tileType}Oneway`, {
        anim: TILE_ANIMATION.topLeft,
      }),
      kaplayContext.area({
        shape: new kaplayContext.Rect(kaplayContext.vec2(0), 16, 3),
      }),
      kaplayContext.body({ isStatic: true }),
      kaplayContext.offscreen(),
      TAG.passthrough,
    ],
    a: () => [
      kaplayContext.sprite(`${tileType}Oneway`, {
        anim: TILE_ANIMATION.topMiddle,
      }),
      kaplayContext.area({
        shape: new kaplayContext.Rect(kaplayContext.vec2(0), 16, 3),
      }),
      kaplayContext.body({ isStatic: true }),
      kaplayContext.offscreen(),
      TAG.passthrough,
    ],
    b: () => [
      kaplayContext.sprite(`${tileType}Oneway`, {
        anim: TILE_ANIMATION.topRight,
      }),
      kaplayContext.area({
        shape: new kaplayContext.Rect(kaplayContext.vec2(0), 16, 3),
      }),
      kaplayContext.body({ isStatic: true }),
      kaplayContext.offscreen(),
      TAG.passthrough,
    ],
    c: () => [
      kaplayContext.sprite(`${tileType}Oneway`, {
        anim: TILE_ANIMATION.middleLeft,
      }),
      kaplayContext.offscreen(),
    ],
    d: () => [
      kaplayContext.sprite(`${tileType}Oneway`, {
        anim: TILE_ANIMATION.middleMiddle,
      }),
      kaplayContext.offscreen(),
    ],
    e: () => [
      kaplayContext.sprite(`${tileType}Oneway`, {
        anim: TILE_ANIMATION.middleRight,
      }),
      kaplayContext.offscreen(),
    ],
    o: () => [
      kaplayContext.sprite(SCENE_ELEMENT_SPRITE.bridge),
      kaplayContext.area(),
      kaplayContext.body({ isStatic: true }),
      kaplayContext.offscreen(),
    ],
    "@": () => [
      kaplayContext.sprite(SCENE_ELEMENT_SPRITE.coin),
      kaplayContext.area(),
      kaplayContext.offscreen(),
      TAG.coin,
    ],
  };
};
