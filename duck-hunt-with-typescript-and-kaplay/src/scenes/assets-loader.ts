import {
  BACKGROUND_SPRITE_ID,
  CURSOR_SPRITE_ID,
  GUN_SHOT_SOUND_ID,
  MENU_SPRITE_ID,
  NES_FONT_ID,
} from "../constants";
import kaplayContext from "../kaplay-context";

// whatever assets are in the "public" folder, Vite allows us to access them as if they were in the root folder
export const loadSceneAssets = () => {
  // load sprites
  kaplayContext.loadSprite(MENU_SPRITE_ID, "./graphics/menu.png");
  kaplayContext.loadSprite(BACKGROUND_SPRITE_ID, "./graphics/background.png");
  kaplayContext.loadSprite(CURSOR_SPRITE_ID, "./graphics/cursor.png");

  // load sounds
  kaplayContext.loadSound(GUN_SHOT_SOUND_ID, ".sounds/gun-shot.wav");

  // load fonts
  kaplayContext.loadFont(
    NES_FONT_ID,
    "./fonts/nintendo-nes-font/nintendo-nes-font.ttf",
  );
};
