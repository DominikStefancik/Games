import type { Vec2 } from "kaplay";

export interface LevelConfig {
  gravity: number;
  playerSpeed: number;
  jumpForce: number;
  playerLivesCount: number;
  playerStartPosition: Vec2;
  currentLevelScene: number;
  isInLastLeveL: boolean;
}
