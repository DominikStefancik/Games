import React, { FC } from "react";
import Cell from "../cell/Cell";
import { StyledStage } from "./StyledStage";

const Stage: FC<{ stage: any[] }> = ({ stage }) => {
  return (
    <StyledStage width={stage[0].length} height={stage.length}>
      {stage.map((row) => {
        return row.map((cell, index) => {
          return <Cell key={index} type={cell[0]} />;
        });
      })}
    </StyledStage>
  );
};

export default Stage;
