import kaplayContext from "../../kaplay-context";
import type { SpiderConfig } from "../models";

export const level1SpiderConfigs: SpiderConfig[] = [
  {
    type: "Green",
    movementRange: 300,
    speed: 2,
    position: kaplayContext.vec2(2000, 300),
  },
  {
    type: "Green",
    movementRange: 150,
    speed: 1,
    position: kaplayContext.vec2(2020, 0),
  },
  {
    type: "Green",
    movementRange: 150,
    speed: 1,
    position: kaplayContext.vec2(3200, 200),
  },
  {
    type: "Green",
    movementRange: 300,
    speed: 2,
    position: kaplayContext.vec2(3500, 300),
  },
  {
    type: "Green",
    movementRange: 300,
    speed: 1,
    position: kaplayContext.vec2(4500, 300),
  },
  {
    type: "Green",
    movementRange: 300,
    speed: 2,
    position: kaplayContext.vec2(5200, 0),
  },
  {
    type: "Green",
    movementRange: 150,
    speed: 1,
    position: kaplayContext.vec2(5700, 400),
  },
  {
    type: "Green",
    movementRange: 150,
    speed: 1,
    position: kaplayContext.vec2(6000, 400),
  },
];
