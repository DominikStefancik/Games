type Direction = "left" | "right";

interface FighterProperties {
  speed: number;
  direction: Direction;
  isDead: boolean;
  isCooldownActive: boolean;
  maxHealthPoints: number;
  // this property helps tracking how health of a figher decreaces
  previousHealthPoints: number;
}

export const initialFighterProps: FighterProperties = {
  speed: 200,
  direction: "left",
  isDead: false,
  isCooldownActive: false,
  maxHealthPoints: 10,
  previousHealthPoints: 10,
};
