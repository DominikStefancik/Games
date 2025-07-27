import {
  ARROW_DOWN_KEY_SPRITE,
  ARROW_LEFT_KEY_SPRITE,
  ARROW_RIGHT_KEY_SPRITE,
  ARROW_UP_KEY_SPRITE,
  BRIDGE_SPRITE,
  COIN_SPRITE,
  CONFIRM_UI_SOUND,
  FOREST_BACKGROUND_SPRITE,
  GRASS_ONEWAY_TILESET_SPRITE,
  GRASS_TILESET_SPRITE,
  LOGO_SPRITE,
  ROUND_FONT,
  SPACE_KEY_SPRITE,
  TILE_ANIMATION,
  WAVE_ANIMATION,
  WAVE_TYPE_SPRITE,
} from "../constants";
import kaplayContext from "../kaplay-context";

export const loadSceneAssets = () => {
  loadFonts();
  loadSounds();
  loadSprites();
};

const loadFonts = () => {
  kaplayContext.loadFont(ROUND_FONT, "./fonts/Round9x13.ttf");
};

const loadSounds = () => {
  kaplayContext.loadSound(CONFIRM_UI_SOUND, "./sounds/confirm-ui.wav");
};

const loadSprites = () => {
  kaplayContext.loadSprite(
    FOREST_BACKGROUND_SPRITE,
    "./graphics/backgrounds/Forest_Background_0.png",
  );
  kaplayContext.loadSprite(LOGO_SPRITE, "./Logo.png");
  kaplayContext.loadSprite(
    ARROW_UP_KEY_SPRITE,
    "./graphics/controls/Arrow_Up_Key_Dark.png",
  );
  kaplayContext.loadSprite(
    ARROW_DOWN_KEY_SPRITE,
    "./graphics/controls/Arrow_Down_Key_Dark.png",
  );
  kaplayContext.loadSprite(
    ARROW_LEFT_KEY_SPRITE,
    "./graphics/controls/Arrow_Left_Key_Dark.png",
  );
  kaplayContext.loadSprite(
    ARROW_RIGHT_KEY_SPRITE,
    "./graphics/controls/Arrow_Right_Key_Dark.png",
  );
  kaplayContext.loadSprite(
    SPACE_KEY_SPRITE,
    "./graphics/controls/Space_Key_Dark.png",
  );

  kaplayContext.loadSprite(
    GRASS_TILESET_SPRITE,
    "./graphics/tilesets/Grass_Tileset.png",
    // the third argument defines how a picture will be devided into frames/slices
    {
      sliceX: 3,
      sliceY: 4,
      anims: {
        [TILE_ANIMATION.topLeft]: 0,
        [TILE_ANIMATION.topMiddle]: 1,
        [TILE_ANIMATION.topRight]: 2,
        [TILE_ANIMATION.middleLeft]: 3,
        [TILE_ANIMATION.middleMiddle]: 4,
        [TILE_ANIMATION.middleRight]: 5,
        [TILE_ANIMATION.bottomLeft]: 6,
        [TILE_ANIMATION.bottomMiddle]: 7,
        [TILE_ANIMATION.bottomRight]: 8,
      },
    },
  );
  kaplayContext.loadSprite(
    GRASS_ONEWAY_TILESET_SPRITE,
    "./graphics/tilesets/Grass_Oneway.png",
    // the third argument defines how a picture will be devided into frames/slices
    {
      sliceX: 3,
      sliceY: 4,
      anims: {
        [TILE_ANIMATION.topLeft]: 0,
        [TILE_ANIMATION.topMiddle]: 1,
        [TILE_ANIMATION.topRight]: 2,
        [TILE_ANIMATION.middleLeft]: 3,
        [TILE_ANIMATION.middleMiddle]: 4,
        [TILE_ANIMATION.middleRight]: 5,
        [TILE_ANIMATION.bottomLeft]: 6,
        [TILE_ANIMATION.bottomMiddle]: 7,
        [TILE_ANIMATION.bottomRight]: 8,
      },
    },
  );
  kaplayContext.loadSprite(BRIDGE_SPRITE, "./graphics/scene-elements/Coin.png");
  kaplayContext.loadSprite(COIN_SPRITE, "./graphics/scene-elements/Bridge.png");
  kaplayContext.loadSprite(
    WAVE_TYPE_SPRITE.water,
    "./graphics/scene-elements/Water.png",
    // the third argument defines how a picture will be devided into frames/slices
    {
      sliceX: 3,
      sliceY: 4,
      anims: {
        [WAVE_ANIMATION]: { from: 0, to: 7, speed: 16, loop: true },
      },
    },
  );
};
