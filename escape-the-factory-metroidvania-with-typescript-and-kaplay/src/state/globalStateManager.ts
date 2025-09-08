interface StateProps {
  playerHealthPoints: number;
  maxPlayerHealthPoints: number;
  isDoubleJumpUnlocked: boolean;
  playerIsInBossFight: boolean;
  isBossDefeated: boolean;
}

const initStateManager = () => {
  const state: StateProps = {
    playerHealthPoints: 3,
    maxPlayerHealthPoints: 3,
    isDoubleJumpUnlocked: false,
    playerIsInBossFight: false,
    isBossDefeated: false,
  };

  return {
    currentState: () => {
      return { ...state };
    },
    setState: (property: keyof StateProps, value: number | boolean) => {
      if (typeof value === "number") {
        (state[property] as number) = value;
      }

      if (typeof value === "boolean") {
        (state[property] as boolean) = value;
      }
    },
  };
};

export const state = initStateManager();
