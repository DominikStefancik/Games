import kaplayContext from "../../kaplay-context";
import type { FishConfig } from "../models";

export const level1FishConfigs: FishConfig[] = [
  {
    type: "Blue",
    movementRange: 300,
    position: kaplayContext.vec2(2595, 600),
  },
  {
    type: "Blue",
    movementRange: 500,
    position: kaplayContext.vec2(2655, 600),
  },
  {
    type: "Purple",
    movementRange: 400,
    position: kaplayContext.vec2(4100, 600),
  },
  {
    type: "Purple",
    movementRange: 500,
    position: kaplayContext.vec2(4220, 800),
  },
  {
    type: "Blue",
    movementRange: 900,
    position: kaplayContext.vec2(5200, 800),
  },
  {
    type: "Blue",
    movementRange: 800,
    position: kaplayContext.vec2(5300, 800),
  },
];
