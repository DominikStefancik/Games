import kaplay, { type KAPLAYCtx } from "kaplay";
import { SCREEN } from "./constants";

const SCALE = 2;

const kaplayContext: KAPLAYCtx = kaplay({
  width: SCREEN.width * SCALE,
  height: SCREEN.height * SCALE,
  /*
   * keeps the aspect ratio of the canvas -> it allows your canvas to be responsive
   * regardless of the screen size, it will respect (keep) the aspect ratio
   */
  letterbox: true,
  scale: SCALE,
  /*
   * if false, we cannot use any Kaplay functions outside of this context object
   * i.e. we will have to call thme by using "kaplayContext.<function_name>"
   * this will prevent name conflicts, where there are some functions coming from Kaplay
   * and some (with the same name) from vanilla Javascript
   */
  global: false,
  background: SCREEN.background,
  debug: true, // sets the debug mode
  debugKey: "d", // specifies which key turns on the debug mode
});

export default kaplayContext;
