import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import { ENTITY_SPRITE, PLAYER_ANIMATIOM, TAG } from "../constants";

export const createPlayer = (params: {
  position: Vec2;
  speed: number;
  jumpForce: number;
  livesCount: number;
  currentLevelScene: number;
  isInLastLeveL: boolean;
}): GameObj => {
  const { position } = params;

  const playerObject = kaplayContext.add([
    kaplayContext.sprite(ENTITY_SPRITE.player, {
      anim: PLAYER_ANIMATIOM.idle,
    }),
    kaplayContext.scale(4),
    kaplayContext.area({
      shape: new kaplayContext.Rect(kaplayContext.vec2(0, 3), 8, 8),
    }),
    kaplayContext.body(),
    kaplayContext.pos(position),
    kaplayContext.anchor("center"),
    TAG.player,
  ]);

  return playerObject;
};
