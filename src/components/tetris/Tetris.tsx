import React, { FC, useState } from "react";
import Stage from "../stage/Stage";
import Display from "../display/Display";
import { StyledTetris, StyledTetrisWrapper } from "./StyledTetris";
import StartButton from "../start-button/StartButton";
import { useTetromino } from "../../hooks/useTetromino";
import { useStage } from "../../hooks/useStage";
import { checkCollision, createStage, RotationDirection } from "../../helpers/gameHelpers";

const Tetris: FC = () => {
  const [dropTime, setDropTime] = useState(null);
  const [isGameOver, setGameOver] = useState(false);

  const [
    tetrominoState,
    updateTetrominoPosition,
    resetTetrominoState,
    rotateTetromino,
  ] = useTetromino();
  const [stage, setStage] = useStage<>(tetrominoState, resetTetrominoState);

  const startGame = () => {
    // Reset everything
    setGameOver(false);
    setStage(createStage());
    resetTetrominoState();
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
  };

  const dropTetromino = () => {
    drop();
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
        case " ": // User hit the Space button
          dropTetromino();
          break;
        default:
          break;
      }
    }
  };

  return (
    <StyledTetrisWrapper role="button" tabIndex="0" onKeyDown={keyDownHandler}>
      <StyledTetris>
        <Stage stage={stage} />
        <aside>
          <Display isGameOver={isGameOver} text={"Score"} />
          <Display isGameOver={isGameOver} text={"Rows"} />
          <Display isGameOver={isGameOver} text={"Level"} />
          {isGameOver && <Display isGameOver={isGameOver} text={"Game Over!!!"} />}
          <StartButton callback={startGame} />
        </aside>
      </StyledTetris>
    </StyledTetrisWrapper>
  );
};

export default Tetris;
