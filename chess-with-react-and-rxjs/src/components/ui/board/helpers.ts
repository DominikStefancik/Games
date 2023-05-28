import { PieceSymbol, Color } from 'chess.js/src/chess';

const PIECE_NAMES = {
  k: 'king',
  q: 'queen',
  b: 'bishop',
  n: 'knight',
  r: 'rook',
  p: 'pawn',
};
const COLOR_NAMES = {
  w: 'white',
  b: 'black',
};
const SQUARE_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];

const getCoordinates = (index: number): { x: number; y: number } => {
  return {
    x: index % 8,
    y: Math.abs(Math.floor(index / 8) - 7),
  };
};

export const isSquareBlack = (index: number): boolean => {
  const { x, y } = getCoordinates(index);

  return (x + y) % 2 === 1;
};

export const getImageName = (piece: PieceSymbol, color: Color): string => {
  return `${COLOR_NAMES[color]}_${PIECE_NAMES[piece]}`;
};

export const getSquarePositionNotation = (index: number): string => {
  const { x, y } = getCoordinates(index);
  const letter = SQUARE_LETTERS[x];

  return `${letter}${y + 1}`;
};
