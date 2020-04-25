export const STAGE_WIDTH = 12;
export const STAGE_HEIGHT = 20;

// a multi-dimensional array which represents stage grid
export const createStage = (): any[] => {
  return Array.from(Array(STAGE_HEIGHT), () => {
    return new Array(STAGE_WIDTH).fill([0, "clear"]);
  });
};
