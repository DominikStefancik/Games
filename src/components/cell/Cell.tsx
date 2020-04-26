import React, { FC } from "react";
import { StyledCell } from "./StyledCell";
import { TETROMINOS } from "../../models/tetromino";

interface CellProps {
  type: number | string;
}

const Cell: FC<CellProps> = ({ type }) => {
  const tetromino = TETROMINOS[type];

  return <StyledCell shape={tetromino.shape} color={tetromino.rgb_colour} />;
};

export default Cell;
