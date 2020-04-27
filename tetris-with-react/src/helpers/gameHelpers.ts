import { Tetromino, TETROMINOS, TetrominoState } from "../models/tetromino";
import { CellState, EMPTY_CELL } from "../models/cell";

export const STAGE_WIDTH = 12;
export const STAGE_HEIGHT = 20;

export enum RotationDirection {
  CLOCKWISE,
  ANTICLOCKWISE,
}

export const STARTING_DROP_TIME_SPEED = 1000;
export const GAME_LEVEL_INCREASE = 10;

export const createStage = (): any[] => {
  // a multi-dimensional array which represents stage grid
  return Array.from(Array(STAGE_HEIGHT), () => {
    return new Array(STAGE_WIDTH).fill(EMPTY_CELL);
  });
};

export const getRandomTetromino = (): Tetromino => {
  const tetrominosKeys = "IJLOSTZ";
  const index = Math.floor(Math.random() * tetrominosKeys.length);
  const randomKey = tetrominosKeys[index];

  return TETROMINOS[randomKey];
};

export const checkCollision = (tetrominoState: TetrominoState, stage, moveX, moveY): boolean => {
  for (let y = 0; y < tetrominoState.shape.length; y++) {
    for (let x = 0; x < tetrominoState.shape[y].length; x++) {
      // 1. Check if we are at thew cell which renders a tetromino's block
      if (tetrominoState.shape[y][x] !== 0) {
        if (
          // 2. Check that our move is inside the game areas height (y)
          // We need to check if we are at the bottom of the stage
          !stage[y + tetrominoState.position.y + moveY] ||
          // 3. Check that our move is inside the game areas width (x)
          !stage[y + tetrominoState.position.y + moveY][x + tetrominoState.position.x + moveX] ||
          // 4. Check if the cell we are moving towards is set to 'clear', otherwise we are colliding with other blocks
          stage[y + tetrominoState.position.y + moveY][x + tetrominoState.position.x + moveX][1] ===
            CellState.MERGED
        ) {
          return true;
        }
      }
    }
  }

  return false;
};

export const setDropTimeSpeed = (level: number): number => {
  return STARTING_DROP_TIME_SPEED / (level + 1) + 200;
};
