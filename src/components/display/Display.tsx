import React, { FC } from "react";
import { StyledDisplay } from "./StyledDisplay";

interface DisplayProps {
  text: string;
  isGameOver: boolean;
}

const Display: FC<DisplayProps> = ({ text, isGameOver }) => {
  return <StyledDisplay isGameOver={isGameOver}>{text}</StyledDisplay>;
};

export default Display;
