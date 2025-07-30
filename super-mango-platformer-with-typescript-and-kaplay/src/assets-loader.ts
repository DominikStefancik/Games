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
  ENTITY_SPRITE,
  PLAYER_ANIMATION,
  STATUS_ELEMENT_SPRITE,
  SPIDER_ANIMATION,
  FISH_ANIMATION,
  FLAME_ANIMATION,
} from "./constants";
import kaplayContext from "./kaplay-context";

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
  kaplayContext.loadSound(SOUND.jump, "./sounds/jump.wav");
  kaplayContext.loadSound(SOUND.hit, "./sounds/hit.wav");
  kaplayContext.loadSound(SOUND.coin, "./sounds/coin.wav");
  kaplayContext.loadSound(SOUND.spiderAttack, "./sounds/spider-attack.mp3");
  kaplayContext.loadSound(SOUND.swingingAxe, "./sounds/swinging-axe.mp3");
};

const loadSprites = () => {
  loadBackgroundSprites();
  kaplayContext.loadSprite(LOGO_SPRITE, "./Logo.png");
  loadControlsSprites();
  loadTilesetSprites();
  loadSceneElementSprites();
  loadStatusElementSprites();
  loadEntitySprites();
};

const loadBackgroundSprites = () => {
  kaplayContext.loadSprite(
    BACKGROUND_SPRITE.forest,
    "./graphics/backgrounds/Forest_Background_0.png",
  );
  kaplayContext.loadSprite(
    BACKGROUND_SPRITE.castle,
    "./graphics/backgrounds/Castle_Background_0.png",
  );
  kaplayContext.loadSprite(
    BACKGROUND_SPRITE.sky0,
    "./graphics/backgrounds/Sky_Background_0.png",
  );
  kaplayContext.loadSprite(
    BACKGROUND_SPRITE.sky1,
    "./graphics/backgrounds/Sky_Background_1.png",
  );
  kaplayContext.loadSprite(
    BACKGROUND_SPRITE.sky2,
    "./graphics/backgrounds/Sky_Background_2.png",
  );
};

const loadControlsSprites = () => {
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
};

const loadTilesetSprites = () => {
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
    TILESET_SPRITE.brickTileset,
    "./graphics/tilesets/Brick_Tileset.png",
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
    TILESET_SPRITE.brickOneway,
    "./graphics/tilesets/Brick_Oneway.png",
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
    TILESET_SPRITE.grassRockTileset,
    "./graphics/tilesets/Grass_Rock_Tileset.png",
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
    TILESET_SPRITE.grassRockOneway,
    "./graphics/tilesets/Grass_Rock_Oneway.png",
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
};

const loadSceneElementSprites = () => {
  kaplayContext.loadSprite(
    SCENE_ELEMENT_SPRITE.water,
    "./graphics/scene-elements/Water.png",
    // the third argument defines how a picture will be devided into frames/slices
    {
      sliceX: 8,
      sliceY: 1,
      anims: {
        [WAVE_ANIMATION]: { from: 0, to: 7, speed: 16, loop: true },
      },
    },
  );
  kaplayContext.loadSprite(
    SCENE_ELEMENT_SPRITE.lava,
    "./graphics/scene-elements/Lava.png",
    // the third argument defines how a picture will be devided into frames/slices
    {
      sliceX: 8,
      sliceY: 1,
      anims: {
        [WAVE_ANIMATION]: { from: 0, to: 7, speed: 16, loop: true },
      },
    },
  );
  kaplayContext.loadSprite(
    SCENE_ELEMENT_SPRITE.clouds,
    "./graphics/scene-elements/Clouds.png",
    // the third argument defines how a picture will be devided into frames/slices
    {
      sliceX: 8,
      sliceY: 1,
      anims: {
        [WAVE_ANIMATION]: { from: 0, to: 7, speed: 16, loop: true },
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
    SCENE_ELEMENT_SPRITE.axe,
    "./graphics/scene-elements/Axe_Trap.png",
  );
};

const loadStatusElementSprites = () => {
  kaplayContext.loadSprite(
    STATUS_ELEMENT_SPRITE.coins,
    "./graphics/status-elements/Coins_Ui.png",
  );
  kaplayContext.loadSprite(
    STATUS_ELEMENT_SPRITE.stars,
    "./graphics/status-elements/Stars_Ui.png",
  );
};

const loadEntitySprites = () => {
  kaplayContext.loadSprite(
    ENTITY_SPRITE.player,
    "./graphics/entities/Player.png",
    {
      sliceX: 4,
      sliceY: 6,
      anims: {
        [PLAYER_ANIMATION.idle]: { from: 0, to: 3, loop: true },
        [PLAYER_ANIMATION.run]: { from: 4, to: 7, loop: true },
        [PLAYER_ANIMATION.jumpUp]: 8,
        [PLAYER_ANIMATION.jumpDown]: 9,
      },
    },
  );
  kaplayContext.loadSprite(
    ENTITY_SPRITE.spiderGreen,
    "./graphics/entities/Spider_1.png",
    {
      sliceX: 3,
      sliceY: 1,
      anims: {
        [SPIDER_ANIMATION.idle]: 0,
        [SPIDER_ANIMATION.crawl]: { from: 0, to: 2, loop: true },
      },
    },
  );
  kaplayContext.loadSprite(
    ENTITY_SPRITE.spiderRed,
    "./graphics/entities/Spider_2.png",
    {
      sliceX: 3,
      sliceY: 1,
      anims: {
        [SPIDER_ANIMATION.idle]: 0,
        [SPIDER_ANIMATION.crawl]: { from: 0, to: 2, loop: true },
      },
    },
  );
  kaplayContext.loadSprite(
    ENTITY_SPRITE.fishBlue,
    "./graphics/entities/Fish_1.png",
    {
      sliceX: 2,
      sliceY: 1,
      anims: {
        [FISH_ANIMATION.jump]: { from: 0, to: 1, loop: true },
      },
    },
  );
  kaplayContext.loadSprite(
    ENTITY_SPRITE.fishPurple,
    "./graphics/entities/Fish_2.png",
    {
      sliceX: 2,
      sliceY: 1,
      anims: {
        [FISH_ANIMATION.jump]: { from: 0, to: 1, loop: true },
      },
    },
  );
  kaplayContext.loadSprite(
    ENTITY_SPRITE.flameYellow,
    "./graphics/entities/Flame_1.png",
    {
      sliceX: 2,
      sliceY: 1,
      anims: {
        [FLAME_ANIMATION.jump]: { from: 0, to: 1, loop: true },
      },
    },
  );
};
