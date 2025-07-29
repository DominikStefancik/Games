import {
  WAVE_ANIMATION,
  SCENE_ELEMENT_SPRITE,
  BACKGROUND_SPRITE,
} from "../../constants";
import { createFish } from "../../entities/fish";
import { createPlayer } from "../../entities/player";
import { createSpiders } from "../../entities/spider";
import kaplayContext from "../../kaplay-context";
import { level1Config } from "../../level-content/level1/config";
import { level1FishConfigs } from "../../level-content/level1/fish-config";
import {
  level1Layout,
  level1Mappings,
} from "../../level-content/level1/leve1-layout";
import { level1SpiderConfigs } from "../../level-content/level1/spiders-config";
import { attachCamera } from "../utils/camera";
import {
  displayCoinCount,
  displayLivesCount,
  displayStatusBox,
} from "../utils/helpers";
import { addBackground, drawLevelLayout, drawWaves } from "./helpers";

export const level1 = () => {
  kaplayContext.setGravity(level1Config.gravity);
  addBackground(BACKGROUND_SPRITE.forest);
  drawLevelLayout(level1Layout, level1Mappings);
  const player = createPlayer(level1Config);
  attachCamera({ objectToAttachTo: player, offsetX: 0, fixedY: 200 });
  createSpiders(level1SpiderConfigs);
  createFish(level1FishConfigs);
  drawWaves(SCENE_ELEMENT_SPRITE.water, WAVE_ANIMATION);
  displayStatusBox();
  displayLivesCount(player);
  displayCoinCount(player);
};
