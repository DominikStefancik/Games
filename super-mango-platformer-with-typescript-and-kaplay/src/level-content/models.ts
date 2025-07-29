import type { Vec2 } from "kaplay";

export interface LevelConfig {
  gravity: number;
  playerSpeed: number;
  jumpForce: number;
  playerLivesCount: number;
  playerStartPosition: Vec2;
  currentLevelScene: number;
  isInLastLeveL: boolean;
  /*
   * This property defines a vertical limit on the screen.
   * If a player's vertical position is over this limit, he is considered dead (e.g. he fell into a water)
   * As the player falls, his vertical position (pos.y) increaces, so if he is dead, his pos.y > limit
   */
  lostLiveLevel: number;
  spiders?: SpiderConfig[];
}

type SpiderType = "Green" | "Red";

export interface SpiderConfig {
  type: SpiderType;
  movementRange: number;
  speed: number;
  position: Vec2;
}
