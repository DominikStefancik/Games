import { Color, PieceSymbol, Square } from 'chess.js/src/chess';

export interface BoardSquare {
  square: Square;
  type: PieceSymbol;
  color: Color;
}
