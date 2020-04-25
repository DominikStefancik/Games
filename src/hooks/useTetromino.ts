import { useCallback, useState } from "react";
import { getRandomTetromino, STAGE_WIDTH } from "../helpers/gameHelpers";
import { NoShape, TetrominoState } from "../models/tetromino";

// custom hook for manipulation a tetronimo
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

  return [tetrominoState, updateTetrominoPosition, resetTetrominoState];
};
