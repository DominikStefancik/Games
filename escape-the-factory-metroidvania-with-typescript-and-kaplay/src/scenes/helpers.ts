import kaplayContext from "../kaplay-context";

export const setBackground = (hexColorCode: string) => {
  kaplayContext.add([
    kaplayContext.rect(kaplayContext.width(), kaplayContext.height()),
    kaplayContext.color(kaplayContext.Color.fromHex(hexColorCode)),
    // the background will stay fixed and will not move as the camera moves
    kaplayContext.fixed(),
  ]);
};
