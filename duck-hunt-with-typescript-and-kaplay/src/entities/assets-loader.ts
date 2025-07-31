import { DOG_ANIMATION, DUCK_ANIMATION, SOUND, SPRITE } from "../constants";
import kaplayContext from "../kaplay-context";

// whatever assets are in the "public" folder, Vite allows us to access them as if they were in the root folder
export const loadEntitiesAssets = () => {
  // load sprites
  kaplayContext.loadSprite(SPRITE.dog, "./graphics/dog.png", {
    sliceX: 4,
    sliceY: 3,
    anims: {
      [DOG_ANIMATION.searching]: {
        from: 0,
        to: 3,
        speed: 6,
        loop: true,
      },
      [DOG_ANIMATION.sniffing]: {
        from: 4,
        to: 5,
        speed: 4,
        loop: true,
      },
      // if an animation consists only of a sigle frame, we just set its number
      [DOG_ANIMATION.detecting]: 6,
      [DOG_ANIMATION.jumping]: {
        from: 7,
        to: 8,
        speed: 6,
      },
      [DOG_ANIMATION.catching]: 9,
      [DOG_ANIMATION.laughing]: {
        from: 10,
        to: 11,
        loop: true,
      },
    },
  });
  kaplayContext.loadSprite(SPRITE.duck, "./graphics/duck.png", {
    sliceX: 8,
    sliceY: 1,
    anims: {
      [DUCK_ANIMATION.flyingDiagonal]: {
        from: 0,
        to: 2,
        loop: true,
      },
      [DUCK_ANIMATION.flyingSide]: {
        from: 3,
        to: 5,
        loop: true,
      },
      // if an animation consists only of a sigle frame, we just set its number
      [DUCK_ANIMATION.shot]: 6,
      [DUCK_ANIMATION.falling]: 7,
    },
  });

  // load sounds
  kaplayContext.loadSound(SOUND.sniffing, "./sounds/sniffing.wav");
  kaplayContext.loadSound(SOUND.barking, "./sounds/barking.wav");
  kaplayContext.loadSound(SOUND.laughing, "./sounds/laughing.wav");
  kaplayContext.loadSound(SOUND.successfulHunt, "./sounds/successful-hunt.wav");
  kaplayContext.loadSound(SOUND.quacking, "./sounds/quacking.wav");
  kaplayContext.loadSound(SOUND.flapping, "./sounds/flapping.ogg");
  kaplayContext.loadSound(SOUND.falling, "./sounds/fall.wav");
  kaplayContext.loadSound(SOUND.impact, "./sounds/impact.wav");
};
