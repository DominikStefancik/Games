import {
  ANIMATION,
  ATLAS_SPRITE,
  ENTITY_SPRITE,
  FONT,
  SOUND,
  TILESET_SPRITE,
} from "./constants";
import kaplayContext from "./kaplay-context";

export const loadSceneAssets = () => {
  loadFonts();
  loadSounds();
  loadSprites();
  loadSpriteAtlases();
};

const loadFonts = () => {
  kaplayContext.loadFont(FONT.glyphmesss, "./fonts/glyphmesss.ttf");
};

const loadSounds = () => {
  kaplayContext.loadSound(SOUND.notify, "./sounds/notify.mp3");
  kaplayContext.loadSound(SOUND.boom, "./sounds/boom.wav");
  kaplayContext.loadSound(SOUND.health, "./sounds/health.wav");
  kaplayContext.loadSound(SOUND.flamethrower, "./sounds/flamethrower.mp3");
};

const loadSprites = () => {
  loadTilesetSprites();
  loadEntitySprites();
};

const loadSpriteAtlases = () => {
  /*
   * When we are loading sprite atlas, we are cutting out a specific portion of a whole image.
   * So we are not loding a whole image, only its part.
   * We have to specify the coordinates of the top left corner where the cut starts,
   * and then the width and height of the area being cut.
   * The unit of the coordinates and dimensions id a pixel in the image.
   */
  kaplayContext.loadSpriteAtlas("./graphics/atlases/ui-elements.png", {
    [ATLAS_SPRITE.healthbar]: {
      x: 16,
      y: 16,
      width: 60,
      height: 48,
      // this will slice/divide the specific area which was cut from the image
      sliceY: 3,
    },
  });
  kaplayContext.loadSpriteAtlas("./graphics/atlases/animations.png", {
    [ATLAS_SPRITE.cartridge]: {
      x: 125,
      y: 145,
      width: 134,
      height: 16,
      // this will slice/divide the specific area which was cut from the image
      sliceX: 8,
      anims: {
        [ANIMATION.cartridge.default]: { from: 0, to: 4, loop: true, speed: 7 },
      },
    },
  });
};

const loadTilesetSprites = () => {
  kaplayContext.loadSprite(
    TILESET_SPRITE.tileset,
    "./graphics/tilesets/tileset.png",
    // the third argument defines how a picture will be devided into frames/slices
    {
      sliceX: 33,
      sliceY: 21,
    },
  );
  kaplayContext.loadSprite(
    TILESET_SPRITE.background,
    "./graphics/tilesets/background.png",
    // the third argument defines how a picture will be devided into frames/slices
    {
      sliceX: 13,
      sliceY: 25,
    },
  );
};

const loadEntitySprites = () => {
  kaplayContext.loadSprite(
    ENTITY_SPRITE.player,
    "./graphics/entities/player.png",
    {
      sliceX: 8,
      sliceY: 9,
      anims: {
        [ANIMATION.player.idle]: { from: 0, to: 7, loop: true },
        [ANIMATION.player.run]: { from: 8, to: 13, loop: true },
        [ANIMATION.player.jump]: { from: 51, to: 51, loop: true },
        [ANIMATION.player.fall]: { from: 54, to: 54, loop: true },
        [ANIMATION.player.attack]: { from: 24, to: 28, speed: 16 },
        [ANIMATION.player.explode]: { from: 64, to: 69 },
      },
    },
  );
  kaplayContext.loadSprite(
    ENTITY_SPRITE.drone,
    "./graphics/entities/drone.png",
    {
      sliceX: 6,
      sliceY: 3,
      anims: {
        [ANIMATION.drone.flying]: { from: 0, to: 3, loop: true },
        [ANIMATION.drone.attack]: { from: 6, to: 11, speed: 16 },
        [ANIMATION.drone.explode]: { from: 12, to: 17 },
      },
    },
  );
  kaplayContext.loadSprite(
    ENTITY_SPRITE.bossBurner,
    "./graphics/entities/boss-burner.png",
    {
      sliceX: 5,
      sliceY: 6,
      anims: {
        [ANIMATION.bossBurner.idle]: { from: 0, to: 3, loop: true },
        [ANIMATION.bossBurner.run]: { from: 6, to: 8, loop: true },
        [ANIMATION.bossBurner.openFire]: { from: 10, to: 14 },
        [ANIMATION.bossBurner.fire]: { from: 15, to: 18, loop: true },
        [ANIMATION.bossBurner.shutFire]: { from: 20, to: 23 },
        [ANIMATION.bossBurner.explode]: { from: 25, to: 29 },
      },
    },
  );
};
