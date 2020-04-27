import React, { FC } from "react";
import Square from "../square/Square";
import { SquareType } from "../../models/square";

interface BoardProps {
  squares: SquareType[];
  onClickHandler: (event: MouseEvent) => void;
}

const styles = {
  border: "5px solid darkblue",
  borderRadius: "10px", // properties are in a Javascript object, we cannot use "-" in the name
  width: "500px",
  height: "500px",
  margin: "0 auto",
  display: "grid",
  gridTemplate: "repeat(3, 1fr) / repeat(3, 1fr)", // creates a grid with 3 rows and 3 columns
};

const Board: FC<BoardProps> = ({ squares, onClickHandler }: BoardProps) => (
  <div style={styles}>
    {squares.map((square, index) => (
      <Square key={index} value={square} onClick={onClickHandler} />
    ))}
  </div>
);

export default Board;
