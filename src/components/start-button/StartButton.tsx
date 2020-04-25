import React, { FC } from "react";
import { StyledStartButton } from "./StyledStartButton";

interface StartButtonProps {
  callback: () => void;
}

const StartButton: FC<StartButtonProps> = ({ callback }) => {
  return <StyledStartButton onClick={callback}>Start Game</StyledStartButton>;
};

export default StartButton;
