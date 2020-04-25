import React, { FC } from "react";
import Cell from "../cell/Cell";
import { NoShape } from "../../models/tetromino";
import { StyledStage } from "./StyledStage";

const Stage: FC<{ stage: any[] }> = ({ stage }) => {
  return (
    <StyledStage width={stage[0].length} height={stage.length}>
      {stage.map((row) => {
        return row.map((cell, index) => {
          return <Cell key={index} type={NoShape} />;
        });
      })}
    </StyledStage>
  );
};

export default Stage;
