import {
  ARROW_DOWN_KEY_SPRITE,
  ARROW_LEFT_KEY_SPRITE,
  ARROW_RIGHT_KEY_SPRITE,
  ARROW_UP_KEY_SPRITE,
  CONFIRM_UI_SOUND,
  FOREST_BACKGROUND_SPRITE,
  LOGO_SPRITE,
  ROUND_FONT,
  SPACE_KEY_SPRITE,
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
};
