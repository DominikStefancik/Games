import React, { FC, useState } from "react";
import Stage from "../stage/Stage";
import Display from "../display/Display";
import { StyledTetris, StyledTetrisWrapper } from "./StyledTetris";
import StartButton from "../start-button/StartButton";
import { useTetronimo } from "../../hooks/useTetronimo";
import { useStage } from "../../hooks/useStage";

const Tetris: FC = () => {
  const [isGameOver, setGameOver] = useState(false);

  const [tetronimo] = useTetronimo();
  const [stage, setStage] = useStage();

  return (
    <StyledTetrisWrapper>
      <StyledTetris>
        <Stage stage={stage} />
        <aside>
          <Display isGameOver={isGameOver} text={"Score"} />
          <Display isGameOver={isGameOver} text={"Rows"} />
          <Display isGameOver={isGameOver} text={"Level"} />
          {isGameOver && <Display isGameOver={isGameOver} text={"Game Over"} />}
          <StartButton callback={() => {}} />
        </aside>
      </StyledTetris>
    </StyledTetrisWrapper>
  );
};

export default Tetris;
