import type { KAPLAYCtx } from "kaplay";
import {
  ATTACK_ANIMATION_ID,
  DYING_ANIMATION_ID,
  FALL_ANIMATION_ID,
  HIT_ANIMATION_ID,
  IDLE_ANIMATION_ID,
  JUMP_ANIMATION_ID,
  NINJA_SPRITE_ID,
  RUN_ANIMATION_ID,
  SAMURAI_SPRITE_ID,
} from "../constants";

export const loadEntitySprites = (context: KAPLAYCtx) => {
  context.loadSprite(
    SAMURAI_SPRITE_ID,
    "./assets/graphics/entities/samurai.png",
    {
      sliceX: 8,
      sliceY: 9,
      anims: {
        [IDLE_ANIMATION_ID]: {
          from: 32,
          to: 39,
          loop: true,
        },
        [RUN_ANIMATION_ID]: {
          from: 48,
          to: 55,
          loop: true,
        },
        [JUMP_ANIMATION_ID]: {
          from: 40,
          to: 41,
          loop: true,
        },
        [FALL_ANIMATION_ID]: {
          from: 24,
          to: 25,
          loop: true,
        },
        [ATTACK_ANIMATION_ID]: {
          from: 0,
          to: 5,
        },
        [DYING_ANIMATION_ID]: {
          from: 16,
          to: 21,
        },
        [HIT_ANIMATION_ID]: {
          from: 56,
          to: 59,
        },
      },
    },
  );

  context.loadSprite(NINJA_SPRITE_ID, "./assets/graphics/entities/ninja.png", {
    sliceX: 8,
    sliceY: 8,
    anims: {
      [IDLE_ANIMATION_ID]: {
        from: 32,
        to: 35,
        loop: true,
      },
      [RUN_ANIMATION_ID]: {
        from: 48,
        to: 55,
        loop: true,
      },
      [JUMP_ANIMATION_ID]: {
        from: 40,
        to: 41,
        loop: true,
      },
      [FALL_ANIMATION_ID]: {
        from: 24,
        to: 25,
        loop: true,
      },
      [ATTACK_ANIMATION_ID]: {
        from: 0,
        to: 3,
      },
      [DYING_ANIMATION_ID]: {
        from: 16,
        to: 22,
      },
      [HIT_ANIMATION_ID]: {
        from: 56,
        to: 58,
      },
    },
  });
};
