import type { GameObj } from "kaplay";
import kaplayContext from "../../kaplay-context";

export const attachCamera = (params: {
  objectToAttachTo: GameObj;
  offsetX: number;
  fixedY: number;
}) => {
  const { objectToAttachTo, offsetX, fixedY } = params;

  kaplayContext.onUpdate(() => {
    kaplayContext.setCamPos(objectToAttachTo.pos.x + offsetX, fixedY);
  });
};
