import type { GameObj, KAPLAYCtx } from "kaplay";
import type { TiledTileLayer } from "../models";
import {
  BACKGROUND_SPRITE_1_ID,
  BACKGROUND_SPRITE_2_ID,
  FENCE_SPRITE_ID,
  OAK_WOODS_TILESET_ID,
  SHOP_SPRITE_ID,
} from "../constants";

export const loadSceneSprites = (context: KAPLAYCtx) => {
  context.loadSprite(
    BACKGROUND_SPRITE_1_ID,
    "./assets/graphics/background/background_layer_1.png",
  );
  context.loadSprite(
    BACKGROUND_SPRITE_2_ID,
    "./assets/graphics/background/background_layer_2.png",
  );
  context.loadSprite(FENCE_SPRITE_ID, "./assets/graphics/fence_1.png");
  context.loadSprite(SHOP_SPRITE_ID, "./assets/graphics/shop_anim.png", {
    sliceX: 6,
    sliceY: 1,
    anims: {
      // "default" is an arbitrary name for an animation
      default: {
        from: 0,
        to: 5,
        loop: true,
      },
    },
  });
  context.loadSprite(
    OAK_WOODS_TILESET_ID,
    "./assets/graphics/tiles/oak_woods_tileset.png",
    { sliceX: 31, sliceY: 22 },
  );
};

export const fetchMapData = async (mapFilePath: string) => {
  if (!mapFilePath.endsWith(".json")) {
    throw new Error("The path is not to a JSON file");
  }

  const response = await fetch(mapFilePath);

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  return await response.json();
};

export const drawTile = (params: {
  context: KAPLAYCtx;
  map: GameObj;
  layer: TiledTileLayer;
  tileWidth: number;
  tileHeight: number;
}) => {
  const { context, layer, map, tileWidth, tileHeight } = params;

  // we will draw tiles in rows and we need to know when each row finishes
  let drawnTilesCount = 0;
  const tilePosition = context.vec2(0, 0);

  for (const tileNumber of layer.data) {
    // check if we need to move to the next row
    if (drawnTilesCount % layer.width === 0) {
      tilePosition.x = 0;
      tilePosition.y += tileHeight;
    } else {
      tilePosition.x += tileWidth;
    }

    drawnTilesCount++;

    // zero "0" in the "data" array says that there is no tile
    if (tileNumber === 0) {
      continue;
    }

    map.add([
      context.sprite(OAK_WOODS_TILESET_ID, { frame: tileNumber - 1 }),
      context.pos(tilePosition),
      context.offscreen(),
      context.anchor("center"),
    ]);
  }
};
