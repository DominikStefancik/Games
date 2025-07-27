import {
  BACKGROUND_SPRITE,
  KEY_CONTROL_SPRITE,
  LOGO_SPRITE,
  ROUND_FONT,
  SOUND,
  TILE_ANIMATION,
  TILESET_SPRITE,
  WAVE_ANIMATION,
  SCENE_ELEMENT_SPRITE,
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
  kaplayContext.loadSound(SOUND.confirmUi, "./sounds/confirm-ui.wav");
};

const loadSprites = () => {
  kaplayContext.loadSprite(
    BACKGROUND_SPRITE.forest,
    "./graphics/backgrounds/Forest_Background_0.png",
  );
  kaplayContext.loadSprite(LOGO_SPRITE, "./Logo.png");
  kaplayContext.loadSprite(
    KEY_CONTROL_SPRITE.arrowUp,
    "./graphics/controls/Arrow_Up_Key_Dark.png",
  );
  kaplayContext.loadSprite(
    KEY_CONTROL_SPRITE.arrowDown,
    "./graphics/controls/Arrow_Down_Key_Dark.png",
  );
  kaplayContext.loadSprite(
    KEY_CONTROL_SPRITE.arrowLeft,
    "./graphics/controls/Arrow_Left_Key_Dark.png",
  );
  kaplayContext.loadSprite(
    KEY_CONTROL_SPRITE.arrowRight,
    "./graphics/controls/Arrow_Right_Key_Dark.png",
  );
  kaplayContext.loadSprite(
    KEY_CONTROL_SPRITE.space,
    "./graphics/controls/Space_Key_Dark.png",
  );

  kaplayContext.loadSprite(
    TILESET_SPRITE.grassTileset,
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
    TILESET_SPRITE.grassOneway,
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
  kaplayContext.loadSprite(
    SCENE_ELEMENT_SPRITE.bridge,
    "./graphics/scene-elements/Bridge.png",
  );
  kaplayContext.loadSprite(
    SCENE_ELEMENT_SPRITE.coin,
    "./graphics/scene-elements/Coin.png",
  );
  kaplayContext.loadSprite(
    SCENE_ELEMENT_SPRITE.water,
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
