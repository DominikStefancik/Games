import {
  BARKING_SOUND_ID,
  CATCHING_ANIMATION_ID,
  DETECTING_ANIMATION_ID,
  DOG_SPRITE_ID,
  DUCK_SPRITE_ID,
  FALLING_SOUND_ID,
  FLAPPING_SOUND_ID,
  FLYING_DIAGONAL_ANIMATION_ID,
  IMPACT_SOUND_ID,
  JUMPING_ANIMATION_ID,
  LAUGHING_ANIMATION_ID,
  LAUGHING_SOUND_ID,
  QUACKING_SOUND_ID,
  SEARCHING_ANIMATION_ID,
  SNIFFING_SOUND_ID,
  SUCCESSFUL_HUNT_SOUND_ID,
} from "../constants";
import kaplayContext from "../kaplay-context";

// whatever assets are in the "public" folder, Vite allows us to access them as if they were in the root folder
export const loadEntitiesAssets = () => {
  // load sprites
  kaplayContext.loadSprite(DOG_SPRITE_ID, "./graphics/dog.png", {
    sliceX: 4,
    sliceY: 3,
    anims: {
      [SEARCHING_ANIMATION_ID]: {
        from: 0,
        to: 3,
        speed: 6,
        loop: true,
      },
      [SNIFFING_SOUND_ID]: {
        from: 4,
        to: 5,
        speed: 4,
        loop: true,
      },
      // if an animation consists only of a sigle frame, we just set its number
      [DETECTING_ANIMATION_ID]: 6,
      [JUMPING_ANIMATION_ID]: {
        from: 7,
        to: 8,
        speed: 6,
      },
      [CATCHING_ANIMATION_ID]: 9,
      [LAUGHING_ANIMATION_ID]: {
        from: 10,
        to: 11,
        loop: true,
      },
    },
  });
  kaplayContext.loadSprite(DUCK_SPRITE_ID, "./graphics/duck.png", {
    sliceX: 8,
    sliceY: 1,
    anims: {
      [FLYING_DIAGONAL_ANIMATION_ID]: {
        from: 0,
        to: 2,
        loop: true,
      },
      [SNIFFING_SOUND_ID]: {
        from: 3,
        to: 5,
        loop: true,
      },
      // if an animation consists only of a sigle frame, we just set its number
      [DETECTING_ANIMATION_ID]: 6,
      [CATCHING_ANIMATION_ID]: 7,
    },
  });

  // load sounds
  kaplayContext.loadSound(SNIFFING_SOUND_ID, "./sounds/sniffing.wav");
  kaplayContext.loadSound(BARKING_SOUND_ID, "./sounds/barking.wav");
  kaplayContext.loadSound(LAUGHING_SOUND_ID, "./sounds/laughing.wav");
  kaplayContext.loadSound(
    SUCCESSFUL_HUNT_SOUND_ID,
    "./sounds/successful-hunt.wav",
  );
  kaplayContext.loadSound(QUACKING_SOUND_ID, "./sounds/quacking.wav");
  kaplayContext.loadSound(FLAPPING_SOUND_ID, "./sounds/flapping.ogg");
  kaplayContext.loadSound(FALLING_SOUND_ID, "./sounds/fall.wav");
  kaplayContext.loadSound(IMPACT_SOUND_ID, "./sounds/impact.wav");
};
