import type { GameObj } from "kaplay";
import kaplayContext from "../kaplay-context";
import { ATLAS_SPRITE, CUSTOM_EVENT } from "../constants";
import { stateManager } from "../state/globalStateManager";

const createHealthBar = (): GameObj => {
  return kaplayContext.make([
    kaplayContext.sprite(ATLAS_SPRITE.healthbar, { frame: 0 }),
    kaplayContext.fixed(),
    kaplayContext.pos(10, 10),
    kaplayContext.scale(4),
    {
      healthPointsToFrameMapping: { 1: 2, 2: 1, 3: 0 },
      setEvents(this: GameObj) {
        this.on(CUSTOM_EVENT.updateHealthBar, () => {
          const currentHealthPoints =
            stateManager.getState().playerHealthPoints;

          if (currentHealthPoints === 0) {
            kaplayContext.destroy(this);
            return;
          }

          this.frame = this.healthPointsToFrameMapping[currentHealthPoints];
        });
      },
    },
  ]);
};

export const healthBar = createHealthBar();
healthBar.setEvents();
healthBar.trigger(CUSTOM_EVENT.updateHealthBar);
