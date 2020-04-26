import { useCallback, useState } from "react";
import {
  checkCollision,
  getRandomTetromino,
  RotationDirection,
  STAGE_WIDTH,
} from "../helpers/gameHelpers";
import { NoShape, TetrominoShape, TetrominoState } from "../models/tetromino";

// custom hook for manipulation the state of a tetromino
export const useTetromino = () => {
  const [tetrominoState, setTetrominoState] = useState<TetrominoState>({
    position: {
      x: 0,
      y: 0,
    },
    shape: NoShape.shape,
    collided: false,
  });

  const updateTetrominoPosition = ({ x, y, collided }) => {
    setTetrominoState((previous) => ({
      ...previous,
      position: { x: previous.position.x + x, y: previous.position.y + y },
      collided,
    }));
  };

  const resetTetrominoState = useCallback(() => {
    setTetrominoState({
      position: {
        x: STAGE_WIDTH / 2 - 2,
        y: 0,
      },
      shape: getRandomTetromino().shape,
      collided: false,
    });
  }, []);

  // This function rotates the tetromino's shape
  const rotateShape = (shape: TetrominoShape, direction: RotationDirection) => {
    // Make rows become columns (transpose)
    const rotatedShape = shape.map((_, index) => shape.map((column) => column[index]));

    // Reverse each row to get a rotated shape
    if (direction === RotationDirection.CLOCKWISE) {
      return rotatedShape.map((row) => row.reverse());
    }

    // Otherwise reverse the matrix
    return rotatedShape.reverse();
  };

  // This function initiates the tetromino's rotation with check for collision
  const rotateTetromino = (stage, direction: RotationDirection) => {
    const clonedState: TetrominoState = JSON.parse(JSON.stringify(tetrominoState));
    clonedState.shape = rotateShape(clonedState.shape, direction);

    // Before setting the new state, we need to check if the rotation is within the boundaries of the stage
    const position = clonedState.position.x;
    let offset = 1;
    while (checkCollision(clonedState, stage, 0, 0)) {
      clonedState.position.x += offset;
      offset = -(offset + (offset > 0 ? 1 : -1));

      if (offset > clonedState.shape[0].length) {
        // if we rotated the shape and it's outside of boundaries, we need to rotate it back
        const oppositeDirection =
          direction === RotationDirection.CLOCKWISE
            ? RotationDirection.ANTICLOCKWISE
            : RotationDirection.CLOCKWISE;
        rotateShape(clonedState.shape, oppositeDirection);
        clonedState.position.x = position; // we set the position to its original value before check

        return; // we cannot rotate, hence we don't set the state
      }
    }

    setTetrominoState(clonedState);
  };

  return [tetrominoState, updateTetrominoPosition, resetTetrominoState, rotateTetromino];
};
