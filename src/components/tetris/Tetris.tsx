import React, { FC, useState } from "react";
import Stage from "../stage/Stage";
import Display from "../display/Display";
import { StyledTetris, StyledTetrisWrapper } from "./StyledTetris";
import StartButton from "../start-button/StartButton";
import { useTetronimo } from "../../hooks/useTetronimo";
import { useStage } from "../../hooks/useStage";
import { createStage } from "../../helpers/gameHelpers";

const Tetris: FC = () => {
  const [isGameOver, setGameOver] = useState(false);

  const [tetronimo, updateTetronimoPosition, resetTetronimo] = useTetronimo();
  const [stage, setStage] = useStage<>();

  const startGame = () => {
    // Reset everything
    setStage(createStage());
    resetTetronimo();
  };

  const moveTetronimo = (direction: number) => {
    updateTetronimoPosition({ x: direction, y: 0 });
  };

  const drop = () => {
    updateTetronimoPosition({ x: 0, y: 1 });
  };

  const dropTetronimo = () => {
    drop();
  };

  const keyDownHandler = (event: KeyboardEvent) => {
    if (!isGameOver) {
      switch (event.key) {
        case "Left": // IE/Edge specific value
        case "ArrowLeft":
          moveTetronimo(-1);
          break;
        case "Right": // IE/Edge specific value
        case "ArrowRight":
          moveTetronimo(1);
          break;
        case "Down": // IE/Edge specific value
        case "ArrowDown":
          dropTetronimo();
          break;
      }
    }
  };

  return (
    <StyledTetrisWrapper role="button" tabIndex="0" onKeyDown={(event) => {}}>
      <StyledTetris>
        <Stage stage={stage} />
        <aside>
          <Display isGameOver={isGameOver} text={"Score"} />
          <Display isGameOver={isGameOver} text={"Rows"} />
          <Display isGameOver={isGameOver} text={"Level"} />
          {isGameOver && <Display isGameOver={isGameOver} text={"Game Over"} />}
          <StartButton callback={() => {}} onClick={startGame()} />
        </aside>
      </StyledTetris>
    </StyledTetrisWrapper>
  );
};

export default Tetris;
