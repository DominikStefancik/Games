import React, { FC, useState } from "react";
import { calculateWinner } from "../../helpers/gameHelpers";
import { HistoryType } from "../../models/board.model";

const styles = {
  width: "200px",
  margin: "20px auto",
};

const Game: FC = () => {
  const [history, setHistory] = useState<HistoryType>([new Array(9).fill(null)]);
  const [stepNumber, setStepNumber] = useState(0);
  const [xIsNext, setXisNext] = useState(true);

  // on each render we will check if there is a winner already
  // we check it from the last state of the board
  const winner = calculateWinner(history[stepNumber]);

  return <div>Game</div>;
};

export default Game;
