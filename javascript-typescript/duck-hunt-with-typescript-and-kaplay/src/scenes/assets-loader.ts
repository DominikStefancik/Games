import { NES_FONT_ID, SOUND, SPRITE } from "../constants";
import kaplayContext from "../kaplay-context";

// whatever assets are in the "public" folder, Vite allows us to access them as if they were in the root folder
export const loadSceneAssets = () => {
  // load sprites
  kaplayContext.loadSprite(SPRITE.menu, "./graphics/menu.png");
  kaplayContext.loadSprite(SPRITE.background, "./graphics/background.png");
  kaplayContext.loadSprite(SPRITE.cursor, "./graphics/cursor.png");
  kaplayContext.loadSprite(SPRITE.textBox, "./graphics/text-box.png");

  // load sounds
  kaplayContext.loadSound(SOUND.forestAmbiance, "./sounds/forest-ambiance.wav");
  kaplayContext.loadSound(SOUND.uiAppear, "./sounds/ui-appear.wav");
  kaplayContext.loadSound(SOUND.gunShot, "./sounds/gun-shot.wav");

  // load fonts
  kaplayContext.loadFont(
    NES_FONT_ID,
    "./fonts/nintendo-nes-font/nintendo-nes-font.ttf",
  );
};
