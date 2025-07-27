import {
  WAVE_ANIMATION,
  SCENE_ELEMENT_SPRITE,
  BACKGROUND_SPRITE,
} from "../../constants";
import {
  level1Layout,
  level1Mappings,
} from "../../level-content/level1/leve1-layout";
import { drawBackground, drawLevelLayout, drawWaves } from "./helpers";

export const level1 = () => {
  drawBackground(BACKGROUND_SPRITE.forest);
  drawLevelLayout(level1Layout, level1Mappings);
  drawWaves(SCENE_ELEMENT_SPRITE.water, WAVE_ANIMATION);
};
