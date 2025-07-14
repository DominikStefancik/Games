import kaplay, { type KAPLAYCtx } from "kaplay";

const kaplayContext: KAPLAYCtx = kaplay({
  width: 256,
  height: 224,
  /*
   * keeps the aspect ratio of the canvas -> it allows your canvas to be responsive
   * regardless of the screen size, it will respect (keep) the aspect ratio
   */
  letterbox: true,
  /*
   * if false, we cannot use any Kaplay functions outside of this context object
   * i.e. we will have to call thme by using "kaplayContext.<function_name>"
   * this will prevent name conflicts, where there are some functions coming from Kaplay
   * and some (with the same name) from vanilla Javascript
   */
  global: false,
  touchToMouse: true, // translates any touch input (e.g. on phone) to a mouse click
  scale: 4,
  /*
   * Ensures that the graphics look still ok on bigget screens. Otherwise it would look blury
   *
   * the "devicePixelRatio" is defined globally in the browser, that's why we can access it without an import
   */
  pixelDensity: devicePixelRatio,
  background: [0, 0, 0],
  debug: true, // sets the debug mode
  debugKey: "d", // specifies which key turns on the debug mode
});

export default kaplayContext;
