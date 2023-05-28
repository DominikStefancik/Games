import UISquare from '@local/components/ui/board/components/USquare';
import UIPiece from '@local/components/ui/board/components/UIPiece';
import { BoardSquare } from '@local/components/non-ui/models';
import { useDrop } from 'react-dnd';
import { movePiece } from '@local/components/non-ui/GameEngine';
import { DraggablePiece, DRAGGABLE_ITEM } from '@local/components/ui/board/models';

interface UIBoardSquareProps {
  square: BoardSquare | null;
  squarePosition: string;
  isBlack: boolean;
}

const UIBoardSquare = ({ square, isBlack, squarePosition }: UIBoardSquareProps) => {
  const backgroundClass = isBlack ? 'square-black' : 'square-white';
  const [, dropReference] = useDrop({
    accept: DRAGGABLE_ITEM,
    drop: (item: DraggablePiece) => {
      movePiece(item.currentPosition, squarePosition);
    },
  });

  return (
    <div className={`${backgroundClass} board-square`} ref={dropReference}>
      <UISquare>
        {square && (
          <UIPiece piece={square.type} color={square.color} piecePosition={squarePosition} />
        )}
      </UISquare>
    </div>
  );
};

export default UIBoardSquare;
