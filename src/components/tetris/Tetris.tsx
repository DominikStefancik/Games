import React, { FC } from "react";
import Stage from "../stage/Stage";
import { createStage } from "../../helpers/gameHelpers";

const Tetris: FC = () => {
  return (
    <div>
      <Stage stage={createStage()} />
    </div>
  );
};

export default Tetris;
