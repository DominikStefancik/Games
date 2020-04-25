import { useEffect, useState } from "react";
import { createStage } from "../helpers/gameHelpers";
import { TetrominoState } from "../models/tetromino";
import { CellState, EMPTY_CELL } from "../models/cell";

// custom hook for manipulating the stage
export const useStage = (tetrominoState: TetrominoState, resetTetromino) => {
  const [stage, setStage] = useState(createStage());

  useEffect(() => {
    const updateStage = (previousStage) => {
      // First, get rid of everything which is on stage
      const newStage = previousStage.map((row) =>
        row.map((cell) => (cell[1] === CellState.CLEAR ? EMPTY_CELL : cell))
      );

      // Then draw the tetromino
      tetrominoState.shape.forEach((row, yIndex) =>
        row.forEach((shapeCellValue, xIndex) => {
          if (shapeCellValue !== 0) {
            newStage[yIndex + tetrominoState.position.y][xIndex + tetrominoState.position.x] = [
              shapeCellValue,
              `${tetrominoState.collided ? CellState.MERGED : CellState.CLEAR}`,
            ];
          }
        })
      );

      return newStage;
    };

    setStage((previousStage) => updateStage(previousStage));
  }, [
    tetrominoState.collided,
    tetrominoState.position.x,
    tetrominoState.position.y,
    tetrominoState.shape,
  ]);

  return [stage, setStage];
};
