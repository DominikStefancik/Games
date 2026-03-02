import UISquare from '@local/components/ui/board/components/USquare';
import UIPiece from '@local/components/ui/board/components/UIPiece';
import { BoardSquare, PendingPromotion, GameState } from '@local/components/non-ui/models';
import { useDrop } from 'react-dnd';
import { DraggablePiece, DRAGGABLE_ITEM } from '@local/components/ui/board/models';
import { handlePieceMove, gameSubject } from '@local/components/non-ui/GameEngine';
import { useEffect, useState } from 'react';
import UIPromotion from '@local/components/ui/board/components/UIPromotion';

interface UIBoardSquareProps {
  square: BoardSquare | null;
  squarePosition: string;
  isBlack: boolean;
}

const UIBoardSquare = ({ square, isBlack, squarePosition }: UIBoardSquareProps) => {
  const [promotion, setPromotion] = useState<PendingPromotion | null>(null);
  useEffect(() => {
    // each square has to subscribe to changes of the game in order to react to a promotion of a pawn
    const gameSubscription = gameSubject.subscribe(({ pendingPromotion }: GameState) =>
      pendingPromotion && pendingPromotion.to === squarePosition
        ? setPromotion(pendingPromotion)
        : setPromotion(null)
    );

    // this returned functions is called when the component is unmounted
    // when the component is unmounted, clean up the subscription
    return () => {
      gameSubscription.unsubscribe();
    };
  }, []);

  const [, dropReference] = useDrop({
    accept: DRAGGABLE_ITEM,
    drop: (item: DraggablePiece) => {
      handlePieceMove(item.currentPosition, squarePosition);
    },
  });

  const backgroundClass = isBlack ? 'square-black' : 'square-white';

  return (
    <div className={`${backgroundClass} board-square`} ref={dropReference}>
      <UISquare>
        {promotion && <UIPromotion pendingPromotion={promotion} />}
        {square && !promotion && (
          <UIPiece piece={square.type} color={square.color} piecePosition={squarePosition} />
        )}
      </UISquare>
    </div>
  );
};

export default UIBoardSquare;
