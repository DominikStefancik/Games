import kaplayContext from "../../kaplay-context";
import type { SpiderConfig } from "../models";

export const level2SpiderConfigs: SpiderConfig[] = [
  {
    type: "Red",
    movementRange: 300,
    speed: 2,
    position: kaplayContext.vec2(2200, 100),
  },
  {
    type: "Red",
    movementRange: 150,
    speed: 1,
    position: kaplayContext.vec2(1900, 0),
  },
  {
    type: "Red",
    movementRange: 150,
    speed: 1,
    position: kaplayContext.vec2(3200, 200),
  },
  {
    type: "Red",
    movementRange: 300,
    speed: 2,
    position: kaplayContext.vec2(3500, 300),
  },
  {
    type: "Red",
    movementRange: 300,
    speed: 2,
    position: kaplayContext.vec2(4500, 300),
  },
];
