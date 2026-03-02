import kaplayContext from "../../kaplay-context";
import type { LevelConfig } from "../models";
import { level1FishConfigs } from "./fish-config";
import { level1SpiderConfigs } from "./spiders-config";

export const level1Config: LevelConfig = {
  gravity: 1400,
  playerSpeed: 400,
  jumpForce: 650,
  playerLivesCount: 3,
  playerStartPosition: kaplayContext.vec2(1500, 100),
  currentLevelScene: 1,
  isInLastLeveL: false,
  lostLiveLevel: 1000,
  spiderConfigs: level1SpiderConfigs,
  fishConfigs: level1FishConfigs,
};
