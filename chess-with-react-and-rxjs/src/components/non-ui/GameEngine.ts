import { Chess } from 'chess.js';
import { BehaviorSubject } from 'rxjs';

const chess = new Chess();

export const gameSubject = new BehaviorSubject({
  board: chess.board(), // creates a representation of a chess board
});

export const movePiece = (positionFrom: string, positionTo: string) => {
  try {
    chess.move({ from: positionFrom, to: positionTo });
    gameSubject.next({ board: chess.board() });
  } catch (error: any) {
    console.warn(`Invalid move from ${positionFrom} to ${positionTo}`);
  }
};
