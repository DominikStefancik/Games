import {
  WAVE_ANIMATION,
  SCENE_ELEMENT_SPRITE,
  BACKGROUND_SPRITE,
} from "../../constants";
import { createPlayer } from "../../entities/player";
import kaplayContext from "../../kaplay-context";
import { level2Config } from "../../level-content/level2/config";
import {
  level2Layout,
  level2Mappings,
} from "../../level-content/level2/leve2-layout";
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
  drawWaves(SCENE_ELEMENT_SPRITE.lava, WAVE_ANIMATION);
  displayStatusBox();
  displayLivesCount(player);
  displayCoinCount(player);
};
