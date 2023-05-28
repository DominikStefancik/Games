import { Chess } from 'chess.js';
import { BehaviorSubject } from 'rxjs';
import { PendingPromotion, GameState } from '@local/components/non-ui/models';

const chess = new Chess();

export const gameSubject = new BehaviorSubject<GameState>({
  board: chess.board(), // creates a representation of a chess board
});

export const initializeGame = () => {
  updateGame();
};

const updateGame = (pendingPromotion?: PendingPromotion) => {
  const newGame = {
    board: chess.board(),
    pendingPromotion,
  };

  gameSubject.next(newGame);
};

export const handlePieceMove = (positionFrom: string, positionTo: string) => {
  const allPossibleMoves = chess.moves({ verbose: true });
  const allPossiblePromotions = allPossibleMoves.filter((move) => move.promotion);
  console.table(allPossibleMoves);
  const isMovePromotion = allPossiblePromotions.some(
    (move) => move.from === positionFrom && move.to === positionTo
  );

  // we need to check if a move we want to make can result in one of possible promotions
  if (isMovePromotion) {
    const pendingPromotion: PendingPromotion = {
      from: positionFrom,
      to: positionTo,
      // since we are promoting a pawn of a certain color, all promotions will have the same color
      color: allPossiblePromotions[0].color,
    };
    updateGame(pendingPromotion);
  }

  const { pendingPromotion } = gameSubject.getValue();

  // move a piece only when we are not in a state of promoting it
  if (!pendingPromotion) {
    movePiece(positionFrom, positionTo);
  }
};

const movePiece = (positionFrom: string, positionTo: string, promotion?: string) => {
  try {
    chess.move({ from: positionFrom, to: positionTo, promotion });
    gameSubject.next({ board: chess.board() });
  } catch (error: any) {
    console.warn(`Invalid move from ${positionFrom} to ${positionTo}`);
  }
};

export const handlePromotion = (
  positionFrom: string,
  positionTo: string,
  promotion: string
): void => {
  movePiece(positionFrom, positionTo, promotion);
};
