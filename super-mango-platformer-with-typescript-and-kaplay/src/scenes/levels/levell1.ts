import {
  FOREST_BACKGROUND_SPRITE,
  WAVE_ANIMATION,
  WAVE_TYPE_SPRITE,
} from "../../constants";
import {
  level1Layout,
  level1Mappings,
} from "../../level-content/level1/leve1-layout";
import { drawBackground, drawLevelLayout, drawWaves } from "./helpers";

export const level1 = () => {
  drawBackground(FOREST_BACKGROUND_SPRITE);
  drawLevelLayout(level1Layout, level1Mappings);
  drawWaves(WAVE_TYPE_SPRITE.water, WAVE_ANIMATION);
};
