import { BACKGROUND_COLOR } from "../constants";
import kaplayContext from "../kaplay-context";
import { createNotificationBox } from "../ui/notificationBox";
import { setBackground } from "./helpers";

export const finalExit = () => {
  setBackground(BACKGROUND_COLOR.outro);
  kaplayContext.add(
    createNotificationBox(
      `You have escaped the factory and finished the game!
      \nThanks for playing!`,
    ),
  );
};
