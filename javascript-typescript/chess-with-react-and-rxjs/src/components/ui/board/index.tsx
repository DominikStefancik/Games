import { BoardSquare } from '@local/root/components/non-ui/models';
import './index.css';
import UIBoardSquare from '@local/components/ui/board/components/UIBoardSquare';
import { isSquareBlack, getSquarePositionNotation } from '@local/components/ui/board/helpers';

interface UIBoardProps {
  board: (BoardSquare | null)[][];
}

const UIBoard = ({ board }: UIBoardProps) => {
  return (
    <div className="board">
      {board.flat().map((piece, index) => {
        return (
          <div key={index} className="square">
            <UIBoardSquare
              square={piece}
              isBlack={isSquareBlack(index)}
              squarePosition={getSquarePositionNotation(index)}
            />
          </div>
        );
      })}
    </div>
  );
};

export default UIBoard;
