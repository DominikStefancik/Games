import { KEY_CONTROL, SCENE } from "../constants";
import kaplayContext from "../kaplay-context";
import { setBackground } from "./helpers";

export const intro = () => {
  setBackground("#a2aed5");
  kaplayContext.onKeyPress(KEY_CONTROL.enter, () => {
    kaplayContext.go(SCENE.room1);
  });
};
