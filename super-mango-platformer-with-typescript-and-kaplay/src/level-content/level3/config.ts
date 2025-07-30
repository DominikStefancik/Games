import kaplayContext from "../../kaplay-context";
import type { LevelConfig } from "../models";
import { level3BirdConfigs } from "./bird-config";

export const level3Config: LevelConfig = {
  gravity: 1400,
  playerSpeed: 400,
  jumpForce: 650,
  playerLivesCount: 5,
  playerStartPosition: kaplayContext.vec2(1500, 100),
  currentLevelScene: 3,
  isInLastLeveL: true,
  lostLiveLevel: 1000,
  birdConfigs: level3BirdConfigs,
};
