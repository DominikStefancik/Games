import type { GameObj, Vec2 } from "kaplay";
import kaplayContext from "../kaplay-context";
import { ANIMATION, ATLAS_SPRITE, SOUND, TAG } from "../constants";
import { stateManager } from "../state/globalStateManager";

export const createHealthCartridge = (position: Vec2): GameObj => {
  const cartridge = kaplayContext.make([
    kaplayContext.sprite(ATLAS_SPRITE.cartridge, {
      anim: ANIMATION.cartridge.default,
    }),
    kaplayContext.area(),
    kaplayContext.anchor("center"),
    kaplayContext.pos(position),
  ]);

  cartridge.onCollide(TAG.player, (player) => {
    kaplayContext.play(SOUND.health, { volume: 0.5 });

    if (player.hp() < stateManager.getState().maxPlayerHealthPoints) {
      player.heal(1);
    }

    kaplayContext.destroy(cartridge);
  });

  return cartridge;
};
