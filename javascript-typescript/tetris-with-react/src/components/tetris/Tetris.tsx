import React, { FC, useState } from "react";
import Stage from "../stage/Stage";
import Display from "../display/Display";
import { StyledTetris, StyledTetrisWrapper } from "./StyledTetris";
import StartButton from "../start-button/StartButton";
import { useTetromino } from "../../hooks/useTetromino";
import { useStage } from "../../hooks/useStage";
import {
  checkCollision,
  createStage,
  GAME_LEVEL_INCREASE,
  RotationDirection,
  setDropTimeSpeed,
  STARTING_DROP_TIME_SPEED,
} from "../../helpers/gameHelpers";
import { useInterval } from "../../hooks/useInterval";
import { useGameStatus } from "../../hooks/useGameStatus";

const Tetris: FC = () => {
  const [dropTime, setDropTime] = useState<>(null);
  const [isGameOver, setGameOver] = useState(false);

  const [
    tetrominoState,
    updateTetrominoPosition,
    resetTetrominoState,
    rotateTetromino,
  ] = useTetromino();

  const [stage, setStage, numberOfRowsCleared] = useStage<>(tetrominoState, resetTetrominoState);

  const [score, setScore, rowsCount, setRowsCount, level, setLevel] = useGameStatus<>(
    numberOfRowsCleared
  );

  useInterval(() => {
    drop();
  }, dropTime);

  const startGame = () => {
    // Reset everything
    setStage(createStage());
    resetTetrominoState();
    setGameOver(false);
    setDropTime(STARTING_DROP_TIME_SPEED);
    setScore(0);
    setRowsCount(0);
    setLevel(0);
  };

  const moveTetromino = (horizontalDirection: number) => {
    if (!checkCollision(tetrominoState, stage, horizontalDirection, 0)) {
      updateTetrominoPosition({ x: horizontalDirection, y: 0, collided: false });
    }
  };

  const drop = () => {
    if (!checkCollision(tetrominoState, stage, 0, 1)) {
      updateTetrominoPosition({ x: 0, y: 1, collided: false });
    } else {
      // If the stage is full of block and a new tetromino's shape is over the top of the stage, the game is over
      if (tetrominoState.position.y < 1) {
        setGameOver(true);
        setDropTime(null);
      }
      updateTetrominoPosition({ x: 0, y: 0, collided: true });
    }

    // Increase the game level when player has cleared given number of rows
    if (rowsCount / level === GAME_LEVEL_INCREASE) {
      setLevel((previousLevel) => previousLevel + 1);

      // Also increase the speed
      setDropTime(setDropTimeSpeed(level));
    }
  };

  const dropTetromino = () => {
    // when a user wants to speed up dropping a tetromino by holding a key, deactivate interval time
    setDropTime(null);
    drop();
  };

  const keyUpHandler = (event) => {
    if (!isGameOver) {
      // when a user wants to stop speeding up dropping a tetromino by holding a key, activate interval time again
      if (event.key === "c" || event.key === "SpaceBar") {
        setDropTime(setDropTimeSpeed(level));
      }
    }
  };

  const keyDownHandler = (event: KeyboardEvent) => {
    if (!isGameOver) {
      switch (event.key) {
        case "Left": // IE/Edge specific value
        case "ArrowLeft":
          moveTetromino(-1);
          break;
        case "Right": // IE/Edge specific value
        case "ArrowRight":
          moveTetromino(1);
          break;
        case "Up": // IE/Edge specific value
        case "ArrowUp":
          rotateTetromino(stage, RotationDirection.CLOCKWISE);
          break;
        case "Down": // IE/Edge specific value
        case "ArrowDown":
          rotateTetromino(stage, RotationDirection.ANTICLOCKWISE);
          break;
        case "SpaceBar": // IE/Edge specific value
        case "c": // User hit the Space button
          dropTetromino();
          break;
        default:
          break;
      }
    }
  };

  return (
    <StyledTetrisWrapper
      role="button"
      tabIndex="0"
      onKeyUp={keyUpHandler}
      onKeyDown={keyDownHandler}
    >
      <StyledTetris>
        <Stage stage={stage} />
        <aside>
          <Display isGameOver={isGameOver} text={`Score: ${score}`} />
          <Display isGameOver={isGameOver} text={`Rows: ${rowsCount}`} />
          <Display isGameOver={isGameOver} text={`Level: ${level}`} />
          {isGameOver && <Display isGameOver={isGameOver} text={"Game Over!!!"} />}
          <StartButton callback={startGame} />
        </aside>
      </StyledTetris>
    </StyledTetrisWrapper>
  );
};

export default Tetris;
