import { useCallback, useState } from "react";
import { getRandomTetromino, STAGE_WIDTH } from "../helpers/gameHelpers";
import { TetronimoShape } from "../models/tetromino";

interface TetronimoState {
  position: { x: number; y: number };
  shape: TetronimoShape;
  collided: boolean;
}

// custom hook for manipulation a tetronimo
export const useTetronimo = () => {
  const [tetronimo, setTetronimo] = useState<TetronimoState>({
    position: {
      x: 0,
      y: 0,
    },
    shape: getRandomTetromino().shape,
    collided: false,
  });

  const updateTetronimoPosition = ({ x, y, collided }) => {
    setTetronimo((previous) => ({
      ...previous,
      position: { x: previous.position.x + x, y: previous.position.y + y },
      collided,
    }));
  };

  const resetTetromino = useCallback(() => {
    setTetronimo({
      position: {
        x: STAGE_WIDTH / 2 - 2,
        y: 0,
      },
      shape: getRandomTetromino().shape,
      collided: false,
    });
  }, []);

  return [tetronimo, updateTetronimoPosition, resetTetromino];
};
