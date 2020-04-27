import React, { FC, useState } from "react";
import { calculateWinner } from "../../helpers/gameHelpers";
import { HistoryType } from "../../models/board.model";
import { O_SYMBOL, X_SYMBOL } from "../../models/square.model";
import Board from "../board/Board";

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

  const clickHandler = (index: number) => {
    // "allMovesInHistory" will contain all the moves until the step we are currently on
    const allMovesInHistory = history.slice(0, stepNumber + 1);
    const currentState = history[stepNumber];
    const currentStateCopy = [...currentState];

    // If a user clicks on an occupied square or the game is won
    if (winner || currentStateCopy[index]) {
      return;
    }

    // Put "X" or "O" on the clicked square
    currentStateCopy[index] = xIsNext ? X_SYMBOL : O_SYMBOL;
    // add a new state to the history
    setHistory([...allMovesInHistory, currentStateCopy]);
    setStepNumber(allMovesInHistory.length);
    setXisNext(!xIsNext);
  };

  // we wrap the board into the React fragment, because we don't want to render a div element
  return (
    <>
      <Board squares={history[stepNumber]} onClickHandler={clickHandler} />
    </>
  );
};

export default Game;
