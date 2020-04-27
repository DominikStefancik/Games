import { useCallback, useEffect, useState } from "react";

export const useGameStatus = (numberOfRowsCleared) => {
  const [score, setScore] = useState<number>(0);
  const [rowsCount, setRowsCount] = useState<number>(0);
  const [level, setLevel] = useState<number>(1); // level starts at 1

  // points obtained after clearing 1, 2, 3 and 4 lines
  const linePoints = [40, 100, 300, 1200];

  const calculateScore = useCallback(() => {
    // We calculate score only if we cleared any rows
    if (numberOfRowsCleared > 0) {
      // This is how original Tetris score is calculated
      setScore((previousScore) => previousScore + linePoints[numberOfRowsCleared - 1] * level);
      setRowsCount((previousRowsCount) => previousRowsCount + numberOfRowsCleared);
    }
  }, [level, linePoints, numberOfRowsCleared]);

  useEffect(() => {
    calculateScore();
  }, [calculateScore, numberOfRowsCleared, score]);

  return [score, setScore, rowsCount, setRowsCount, level, setLevel];
};
