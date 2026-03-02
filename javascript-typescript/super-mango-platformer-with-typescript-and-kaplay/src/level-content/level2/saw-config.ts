import kaplayContext from "../../kaplay-context";
import type { SawConfig } from "../models";

export const level2SawConfigs: SawConfig[] = [
  {
    position: kaplayContext.vec2(8000, 350),
    movementRange: 300,
  },
  {
    position: kaplayContext.vec2(9000, 350),
    movementRange: 500,
  },
];
