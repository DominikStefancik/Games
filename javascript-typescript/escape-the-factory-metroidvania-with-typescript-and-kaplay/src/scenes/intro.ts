import { BACKGROUND_COLOR, KEY_CONTROL, SCENE } from "../constants";
import kaplayContext from "../kaplay-context";
import { createNotificationBox } from "../ui/notificationBox";
import { setBackground } from "./helpers";

export const intro = () => {
  setBackground(BACKGROUND_COLOR.intro);

  kaplayContext.add(
    createNotificationBox(`Escape the factory!\n\nUse arrow left and right keys to move,\narrow up key to jump and space to attack
      \nPress Enter to start!
      \n
      \nMADE BY DOMINIK STEFANCIK`),
  );

  kaplayContext.onKeyPress(KEY_CONTROL.enter, () => {
    kaplayContext.go(SCENE.room1, { exitName: null });
  });
};
