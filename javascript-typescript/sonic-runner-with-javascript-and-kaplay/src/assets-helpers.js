import {
  ANIMATION_JUMP,
  ANIMATION_RUN,
  ANIMATION_SPIN,
  CHEMICAL_BACKGROUND_SPRITE_ID,
  CITY_SOUND_ID,
  DESTROY_SOUND_ID,
  HURT_SOUND_ID,
  HYPER_RING_SOUND_ID,
  JUMP_SOUND_ID,
  MANIA_FONT_ID,
  MOTOBUG_SPRITE_ID,
  PLATFORMS_SPRITE_ID,
  RING_SOUND_ID,
  RING_SPRITE_ID,
  SONIC_SPRITE_ID,
} from "./constants";
import kaplayContext from "./kaplay-context";

export const loadAssets = () => {
  // "loadSprite" method imports a visual asset, e.g. an image
  kaplayContext.loadSprite(
    CHEMICAL_BACKGROUND_SPRITE_ID,
    "graphics/chemical-background.png",
  );
  kaplayContext.loadSprite(PLATFORMS_SPRITE_ID, "graphics/platforms.png");

  // sprite sheet is an image which contains multiple frames (sprites)
  // is used when we want to define an animation
  kaplayContext.loadSprite(SONIC_SPRITE_ID, "graphics/sonic.png", {
    // number of frames in a row
    sliceX: 8,
    // number of frames per column
    sliceY: 2,
    // define your animations created from the frames in the sprite sheet
    anims: {
      // "run" is a custom name if an animation
      [ANIMATION_RUN]: {
        // the frame the animation starts from
        from: 0,
        // the final frame the animation goes to
        to: 7,
        // specifies if the animation shoulb loop indefinitely until we stop it
        loop: true,
        // specifies the speed at which the animation will be played
        speed: 30, // 30 frames per second
      },
      // "jump" is a custom name if an animation
      [ANIMATION_JUMP]: {
        from: 8,
        to: 15,
        loop: true,
        speed: 100,
      },
    },
  });

  kaplayContext.loadSprite(RING_SPRITE_ID, "graphics/ring.png", {
    sliceX: 16,
    sliceY: 1,
    anims: {
      // "spin" is a custom name if an animation
      [ANIMATION_SPIN]: {
        from: 0,
        to: 15,
        loop: true,
        speed: 30,
      },
    },
  });

  kaplayContext.loadSprite(MOTOBUG_SPRITE_ID, "graphics/motobug.png", {
    sliceX: 5,
    sliceY: 1,
    anims: {
      // "run" is a custom name if an animation
      [ANIMATION_RUN]: {
        from: 0,
        to: 4,
        loop: true,
        speed: 8,
      },
    },
  });

  // "loadFont" method imports a font asset which is a .tff file
  kaplayContext.loadFont(MANIA_FONT_ID, "fonts/mania.ttf");

  // "loadSound" method imports a sound asset, e.g. a music file
  kaplayContext.loadSound(CITY_SOUND_ID, "sounds/City.mp3");
  kaplayContext.loadSound(DESTROY_SOUND_ID, "sounds/Destroy.wav");
  kaplayContext.loadSound(HURT_SOUND_ID, "sounds/Hurt.wav");
  kaplayContext.loadSound(HYPER_RING_SOUND_ID, "sounds/HyperRing.wav");
  kaplayContext.loadSound(JUMP_SOUND_ID, "sounds/Jump.wav");
  kaplayContext.loadSound(RING_SOUND_ID, "sounds/Ring.wav");
};
