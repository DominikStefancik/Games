import kaplayContext from "../../kaplay-context";
import type { LevelConfig } from "../models";

export const level2Config: LevelConfig = {
  gravity: 1400,
  playerSpeed: 400,
  jumpForce: 650,
  playerLivesCount: 3,
  playerStartPosition: kaplayContext.vec2(1500, 100),
  currentLevelScene: 2,
  isInLastLeveL: false,
  lostLiveLevel: 1000,
};
