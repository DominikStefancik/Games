import {
  BACKGROUND_SPRITE_ID,
  MENU_SPRITE_ID,
  NES_FONT_ID,
} from "../constants";
import kaplayContext from "../kaplay-context";

// whatever assets are in the "public" folder, Vite allows us to access them as if they were in the root folder
export const loadSceneAssets = () => {
  kaplayContext.loadSprite(MENU_SPRITE_ID, "./graphics/menu.png");
  kaplayContext.loadSprite(BACKGROUND_SPRITE_ID, "./graphics/background.png");
  kaplayContext.loadFont(
    NES_FONT_ID,
    "./fonts/nintendo-nes-font/nintendo-nes-font.ttf",
  );
};
