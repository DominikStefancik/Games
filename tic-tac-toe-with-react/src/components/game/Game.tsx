import React, { FC, useState } from "react";
import { calculateWinner } from "../../helpers/gameHelpers";
import { HistoryType } from "../../models/board.model";
import { O_SYMBOL, SquareType, X_SYMBOL } from "../../models/square.model";
import Board from "../board/Board";

const styles = {
  width: "200px",
  margin: "20px auto",
};

const Game: FC = () => {
  const [history, setHistory] = useState<HistoryType>([new Array(9).fill(null)]);
  const [stepNumber, setStepNumber] = useState(0);
  const [currentSymbol, setCurrentSymbol] = useState<SquareType>(X_SYMBOL);

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
    currentStateCopy[index] = currentSymbol;
    // add a new state to the history
    setHistory([...allMovesInHistory, currentStateCopy]);
    setStepNumber(allMovesInHistory.length);
    setCurrentSymbol(currentSymbol === X_SYMBOL ? O_SYMBOL : X_SYMBOL);
  };

  // we wrap the board into the React fragment, because we don't want to render a div element
  return (
    <>
      <Board squares={history[stepNumber]} onClickHandler={clickHandler} />
      <div style={styles}>{winner ? "Winner: " + winner : "Next player: " + currentSymbol}</div>
    </>
  );
};

export default Game;
