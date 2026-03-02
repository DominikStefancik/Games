import { Color, PieceSymbol, Square } from 'chess.js/src/chess';

export interface GameState {
  board: (BoardSquare | null)[][];
  pendingPromotion?: PendingPromotion;
}

export interface BoardSquare {
  square: Square;
  type: PieceSymbol;
  color: Color;
}

export interface PendingPromotion {
  from: string;
  to: string;
  color: Color;
}
