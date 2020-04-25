import { useEffect, useState } from "react";
import { createStage } from "../helpers/gameHelpers";
import { TetrominoState } from "../models/tetromino";
import { CellState, EMPTY_CELL } from "../models/cell";

// custom hook for manipulating the stage
export const useStage = (tetronimoState: TetrominoState, resetTetronimo) => {
  const [stage, setStage] = useState(createStage());

  useEffect(() => {
    const updateStage = (previousStage) => {
      // First, get rid of everything which is on stage
      const newStage = previousStage.map((row) =>
        row.map((cell) => (cell[1] === CellState.CLEAR ? EMPTY_CELL : cell))
      );

      // Then draw the tetromino
      tetronimoState.shape.forEach((row, yIndex) =>
        row.forEach((shapeCellValue, xIndex) => {
          if (shapeCellValue !== 0) {
            newStage[yIndex + tetronimoState.position.y][xIndex + tetronimoState.position.x] = [
              shapeCellValue,
              `${tetronimoState.collided ? CellState.MERGED : CellState.CLEAR}`,
            ];
          }
        })
      );

      return newStage;
    };

    setStage((previousStage) => updateStage(previousStage));
  }, [
    tetronimoState.collided,
    tetronimoState.position.x,
    tetronimoState.position.y,
    tetronimoState.shape,
  ]);

  return [stage, setStage];
};
