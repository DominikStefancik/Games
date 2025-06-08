import kaplayContext from "./kaplay-context";

// "loadSprite" imports a visual asset, e.g. an image
kaplayContext.loadSprite(
  "chemical-background",
  "graphics/chemical-background.png",
);
kaplayContext.loadSprite("platforms", "graphics/platforms.png");

// sprite sheet is an image which contains multiple frames (sprites)
// is used when we want to define an animation
kaplayContext.loadSprite("sonic", "graphics/sonic.png", {
  // number of frames in a row
  sliceX: 8,
  // number of frames per column
  sliceY: 2,
  // define your animations created from the frames in the sprite sheet
  anims: {
    // "run" is a custom name if an animation
    run: {
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
    jump: {
      from: 8,
      to: 15,
      loop: true,
      speed: 100,
    },
  },
});

kaplayContext.loadSprite("ring", "graphics/ring.png", {
  sliceX: 16,
  sliceY: 1,
  anims: {
    // "spin" is a custom name if an animation
    spin: {
      from: 0,
      to: 15,
      loop: true,
      speed: 30,
    },
  },
});

kaplayContext.loadSprite("motobug", "graphics/ring.png", {
  sliceX: 5,
  sliceY: 1,
  anims: {
    // "run" is a custom name if an animation
    run: {
      from: 0,
      to: 4,
      loop: true,
      speed: 8,
    },
  },
});

// "loadFont" imports a font asset which is a .tff file
kaplayContext.loadFont("mania", "fonts/mania.ttf");

// "loadSound" imports a sound asset, e.g. a music file
kaplayContext.loadSound("city", "sounds/City.mp3");
kaplayContext.loadSound("destroy", "sounds/Destroy.wav");
kaplayContext.loadSound("hurt", "sounds/Hurt.wav");
kaplayContext.loadSound("hyper-ring", "sounds/HyperRing.wav");
kaplayContext.loadSound("jump", "sounds/Jump.wav");
kaplayContext.loadSound("ring", "sounds/Ring.wav");
