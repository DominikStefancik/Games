import { useState } from "react";
import { getRandomTetromino } from "../helpers/gameHelpers";

// custom hook for manipulation a tetronimo
export const useTetronimo = () => {
  const [tetronimo, setTetronimo] = useState({
    position: {
      x: 0,
      y: 0,
    },
    shape: getRandomTetromino().shape,
    collided: false,
  });

  return [tetronimo];
};
