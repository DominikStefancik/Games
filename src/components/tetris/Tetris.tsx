import React, { FC } from "react";
import Stage from "../stage/Stage";
import { createStage } from "../../helpers/gameHelpers";
import { StyledTetris, StyledTetrisWrapper } from "./StyledTetris";

const Tetris: FC = () => {
  return (
    <StyledTetrisWrapper>
      <StyledTetris>
        <Stage stage={createStage()} />
        <aside>
          <div>Tetris</div>
        </aside>
      </StyledTetris>
    </StyledTetrisWrapper>
  );
};

export default Tetris;
