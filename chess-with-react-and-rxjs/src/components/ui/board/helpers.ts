import { PieceSymbol, Color } from 'chess.js/src/chess';

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
  const fullNames = {
    k: 'king',
    q: 'queen',
    b: 'bishop',
    n: 'knight',
    r: 'rook',
    p: 'pawn',
  };
  const fullColorNames = {
    w: 'white',
    b: 'black',
  };

  return `${fullColorNames[color]}_${fullNames[piece]}.png`;
};
