import kaplay from "kaplay";

const kaplayContext = kaplay({
  width: 1920,
  height: 1080,
  letterbox: true, // keeps the aspect ratio of the canvas
  background: [0, 0, 0],
  global: false,
  touchToMouse: true, // translates any touch input (e.g. on phone) to a mouse click
  // defines a concrete buttons for input bindings
  buttons: {
    jumpKey: {
      keyboard: ["space"], // you define multiple keys which will serve as a jump key
      mouse: "left",
    },
  },
  debugKey: "d", // specifies which key turns on the debug mode
  debug: true, // sets the debug mode
});

export default kaplayContext;
