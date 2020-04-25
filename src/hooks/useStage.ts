import { useState } from "react";
import { createStage } from "../helpers/gameHelpers";

// custom hook for manipulating the stage
export const useStage = () => {
  const [stage, setStage] = useState(createStage());

  return [stage];
};
