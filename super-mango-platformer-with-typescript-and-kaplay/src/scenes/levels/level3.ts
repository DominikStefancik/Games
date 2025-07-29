import {
  WAVE_ANIMATION,
  SCENE_ELEMENT_SPRITE,
  BACKGROUND_SPRITE,
} from "../../constants";
import { createPlayer } from "../../entities/player";
import kaplayContext from "../../kaplay-context";
import { level3Config } from "../../level-content/level3/config";
import {
  level3Layout,
  level3Mappings,
} from "../../level-content/level3/leve3-layout";
import { attachCamera } from "../utils/camera";
import {
  displayCoinCount,
  displayLivesCount,
  displayStatusBox,
} from "../utils/helpers";
import { addBackground, drawLevelLayout, drawWaves } from "./helpers";

export const level3 = () => {
  kaplayContext.setGravity(level3Config.gravity);
  addBackground(BACKGROUND_SPRITE.sky0);
  addBackground(BACKGROUND_SPRITE.sky1);
  addBackground(BACKGROUND_SPRITE.sky2);
  drawLevelLayout(level3Layout, level3Mappings);
  const player = createPlayer(level3Config);
  attachCamera({ objectToAttachTo: player, offsetX: 0, fixedY: 200 });
  drawWaves(SCENE_ELEMENT_SPRITE.clouds, WAVE_ANIMATION);
  displayStatusBox();
  displayLivesCount(player);
  displayCoinCount(player);
};
