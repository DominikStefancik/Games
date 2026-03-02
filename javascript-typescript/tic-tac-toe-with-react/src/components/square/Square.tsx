import React, { FC } from "react";
import { SquareType } from "../../models/square.model";

interface SquareProps {
  value: SquareType;
  onClickHandler: () => void;
}

const styles = {
  background: "lightblue",
  border: "5px solid darkblue",
  fontSize: "50px",
  fontWeight: 800,
  cursor: "pointer",
  outline: "none",
};

const Square: FC<SquareProps> = ({ value, onClickHandler }: SquareProps) => (
  <button style={styles} onClick={onClickHandler}>
    {value}
  </button>
);

export default Square;
