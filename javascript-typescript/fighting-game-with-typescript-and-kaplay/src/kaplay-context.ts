import kaplay from "kaplay";

const kaplayContext = kaplay({
  width: 1280,
  height: 720,
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
  debug: true, // sets the debug mode
  debugKey: "g", // specifies which key turns on the debug mode
});

export default kaplayContext;
