import {
  WAVE_ANIMATION,
  SCENE_ELEMENT_SPRITE,
  BACKGROUND_SPRITE,
} from "../../constants";
import { createFlames } from "../../entities/flame";
import { createPlayer } from "../../entities/player";
import { createSpiders } from "../../entities/spider";
import kaplayContext from "../../kaplay-context";
import { level2Config } from "../../level-content/level2/config";
import { level2FlameConfigs } from "../../level-content/level2/flame-config";
import {
  level2Layout,
  level2Mappings,
} from "../../level-content/level2/leve2-layout";
import { level2SpiderConfigs } from "../../level-content/level2/spiders-config";
import { attachCamera } from "../utils/camera";
import {
  displayCoinCount,
  displayLivesCount,
  displayStatusBox,
} from "../utils/helpers";
import { addBackground, drawLevelLayout, drawWaves } from "./helpers";

export const level2 = () => {
  kaplayContext.setGravity(level2Config.gravity);
  addBackground(BACKGROUND_SPRITE.castle);
  drawLevelLayout(level2Layout, level2Mappings);
  const player = createPlayer(level2Config);
  attachCamera({ objectToAttachTo: player, offsetX: 0, fixedY: 200 });
  createSpiders(level2SpiderConfigs);
  createFlames(level2FlameConfigs);
  drawWaves(SCENE_ELEMENT_SPRITE.lava, WAVE_ANIMATION);
  displayStatusBox();
  displayLivesCount(player);
  displayCoinCount(player);
};
