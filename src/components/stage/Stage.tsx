import React, { FC } from "react";
import Cell from "../cell/Cell";

const Stage: FC<{ stage: any[] }> = ({ stage }) => {
  return (
    <div>
      {stage.map((row) => {
        return row.map((cell, index) => {
          return <Cell key={index} />;
        });
      })}
    </div>
  );
};

export default Stage;
