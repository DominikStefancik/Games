import type { GameObj } from "kaplay";
import kaplayContext from "../kaplay-context";

export const makeEntityBlink = async (
  entity: GameObj,
  timespan: number = 0.1,
) => {
  await kaplayContext.tween(
    entity.opacity,
    0,
    timespan,
    (newValue) => (entity.opacity = newValue),
    kaplayContext.easings.linear,
  );

  kaplayContext.tween(
    entity.opacity,
    1,
    timespan,
    (newValue) => (entity.opacity = newValue),
    kaplayContext.easings.linear,
  );
};
