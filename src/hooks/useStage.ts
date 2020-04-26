import { useEffect, useState } from "react";
import { createStage } from "../helpers/gameHelpers";
import { TetrominoState } from "../models/tetromino";
import { CellState, EMPTY_CELL } from "../models/cell";

// custom hook for manipulating the stage
export const useStage = (tetrominoState: TetrominoState, resetTetrominoState) => {
  const [stage, setStage] = useState(createStage());
  const [numberOfRowsCleared, setNumberOfRowsCleared] = useState(0);

  useEffect(() => {
    setNumberOfRowsCleared(0);

    // this function gets a new updated stage and checks if it contains full rows
    // then it returns a new stage without full rows
    const sweepFullRows = (newStage) => {
      return newStage.reduce((accumulator, row) => {
        const isRowFull: boolean = row.reduce((containsNoZero, cell) => {
          return containsNoZero && cell[0] !== 0;
        }, true);

        // if the row is full, we will not push it into the accumulator array
        // instead we will add an empty row on the top of the accumulator
        if (isRowFull) {
          setNumberOfRowsCleared((previous) => previous + 1);
          accumulator.unshift(new Array(newStage[0].length).fill(EMPTY_CELL));
        } else {
          // row is not full, push it as it is into the accumulator
          accumulator.push(row);
        }

        return accumulator;
      }, []);
    };

    const updateStage = (previousStage) => {
      // First, get rid of everything which is on stage
      const newStage = previousStage.map((row) =>
        row.map((cell) => (cell[1] === CellState.CLEAR ? EMPTY_CELL : cell))
      );

      // Then draw the tetromino's shape
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

      if (tetrominoState.collided) {
        resetTetrominoState();
        return sweepFullRows(newStage);
      }

      return newStage;
    };

    setStage((previousStage) => updateStage(previousStage));
  }, [tetrominoState, resetTetrominoState]);

  return [stage, setStage, numberOfRowsCleared];
};
