import React, { FC } from "react";
import Stage from "../stage/Stage";
import Display from "../display/Display";
import { createStage } from "../../helpers/gameHelpers";
import { StyledTetris, StyledTetrisWrapper } from "./StyledTetris";
import StartButton from "../start-button/StartButton";

const Tetris: FC = () => {
  return (
    <StyledTetrisWrapper>
      <StyledTetris>
        <Stage stage={createStage()} />
        <aside>
          <Display isGameOver={false} text={"Score"} />
          <Display isGameOver={false} text={"Rows"} />
          <Display isGameOver={false} text={"Level"} />
          <StartButton callback={() => {}} />
        </aside>
      </StyledTetris>
    </StyledTetrisWrapper>
  );
};

export default Tetris;
