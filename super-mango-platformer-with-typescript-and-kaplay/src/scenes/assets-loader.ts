import {
  CONFIRM_UI_SOUND,
  FOREST_BACKGROUND_SPRITE,
  LOGO_SPRITE,
  ROUND_FONT,
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
};
