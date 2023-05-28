import UISquare from '@local/components/ui/board/components/USquare';
import UIPiece from '@local/components/ui/board/components/UIPiece';
import { BoardSquare } from '@local/components/non-ui/models';

interface UIBoardSquareProps {
  square: BoardSquare | null;
  isBlack: boolean;
}

const UIBoardSquare = ({ square, isBlack }: UIBoardSquareProps) => {
  const backgroundClass = isBlack ? 'square-black' : 'square-white';

  return (
    <div className={`${backgroundClass} board-square`}>
      <UISquare>{square && <UIPiece piece={square.type} color={square.color} />}</UISquare>
    </div>
  );
};

export default UIBoardSquare;
