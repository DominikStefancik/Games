import type { CompList, GameObj, LevelOpt, Vec2 } from "kaplay";
import kaplayContext from "../../kaplay-context";

export const drawBackground = (spriteName: string) => {
  kaplayContext.add([
    kaplayContext.sprite(spriteName),
    kaplayContext.scale(4),
    /*
     * The "fixed()" component ensures that a backround picture will not move when a camera moves
     * Othewise, if camera moves i.e. to left, the backround picture will disappear
     */
    kaplayContext.fixed(),
  ]);
};

export const drawLevelLayout = (
  levelLayout: string[][],
  mappings: {
    [symbol: string]: (position: Vec2) => CompList<any>;
  },
) => {
  const layerSettings: LevelOpt = {
    tileWidth: 16,
    tileHeight: 12,
    tiles: mappings,
  };
  const map: GameObj[] = [];

  for (const layerLayout of levelLayout) {
    // the "addLevel()" method draws a map and retuns it as a game object
    map.push(kaplayContext.addLevel(layerLayout, layerSettings));
  }

  for (const layer of map) {
    // the "use()" method allows us to add components to a game object after it was created
    layer.use(kaplayContext.scale(4));
  }
};

/*
 * Waves are rendered only once and they are fixed.
 * Then when a camera is moving the screen, the waves move with it.
 */
export const drawWaves = (type: string, animation: string) => {
  let offset = -100;

  for (let index = 0; index < 21; index++) {
    kaplayContext.add([
      kaplayContext.sprite(type, { anim: animation }),
      kaplayContext.scale(4),
      kaplayContext.pos(offset, 600),
      kaplayContext.fixed(),
    ]);
    offset += 64;
  }
};
