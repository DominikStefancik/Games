import {
  WAVE_ANIMATION,
  SCENE_ELEMENT_SPRITE,
  BACKGROUND_SPRITE,
} from "../../constants";
import { createPlayer } from "../../entities/player";
import kaplayContext from "../../kaplay-context";
import { level1Config } from "../../level-content/level1/config";
import {
  level1Layout,
  level1Mappings,
} from "../../level-content/level1/leve1-layout";
import { attachCamera } from "../utils/camera";
import {
  displayCoinCount,
  displayLivesCount,
  displayStatusBox,
} from "../utils/helpers";
import { drawBackground, drawLevelLayout, drawWaves } from "./helpers";

export const level1 = () => {
  kaplayContext.setGravity(1400);
  drawBackground(BACKGROUND_SPRITE.forest);
  drawLevelLayout(level1Layout, level1Mappings);
  const player = createPlayer(level1Config);
  attachCamera({ objectToAttachTo: player, offsetX: 0, fixedY: 200 });
  drawWaves(SCENE_ELEMENT_SPRITE.water, WAVE_ANIMATION);
  displayStatusBox();
  displayLivesCount(player);
  displayCoinCount(player);
};
