import { PieceSymbol } from 'chess.js/src/chess';

export const PIECE_NAMES = {
  k: 'king',
  q: 'queen',
  b: 'bishop',
  n: 'knight',
  r: 'rook',
  p: 'pawn',
};

export const COLOR_NAMES = {
  w: 'white',
  b: 'black',
};

export const SQUARE_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

export const DRAGGABLE_ITEM = 'piece';

export const PROMOTION_PIECES: PieceSymbol[] = ['b', 'n', 'r', 'q'];

export interface DraggablePiece {
  id: string;
  currentPosition: string;
}
