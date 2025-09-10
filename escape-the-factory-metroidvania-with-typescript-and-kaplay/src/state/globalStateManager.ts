interface StateProps {
  playerHealthPoints: number;
  maxPlayerHealthPoints: number;
  isDoubleJumpUnlocked: boolean;
  isPlayerInFightWithBoss: boolean;
  isBossDefeated: boolean;
}

const initStateManager = () => {
  const state: StateProps = {
    playerHealthPoints: 3,
    maxPlayerHealthPoints: 3,
    isDoubleJumpUnlocked: false,
    isPlayerInFightWithBoss: false,
    isBossDefeated: false,
  };

  return {
    getState: (): StateProps => {
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
