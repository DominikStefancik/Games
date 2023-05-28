import { PendingPromotion } from '@local/components/non-ui/models';
import { PROMOTION_PIECES } from '@local/components/ui/board/models';
import { getImageName } from '@local/components/ui/board/helpers';
import UISquare from '@local/components/ui/board/components/USquare';
import { handlePromotion } from '@local/components/non-ui/GameEngine';

interface UIPromotionProps {
  pendingPromotion: PendingPromotion;
}

const UIPromotion = ({ pendingPromotion }: UIPromotionProps) => {
  const { from, to, color } = pendingPromotion;

  return (
    <div className="board">
      {PROMOTION_PIECES.map((piece, index) => (
        <div key={index} className="promote-square">
          <UISquare>
            <div className="piece-container">
              <img
                src={`./src/assets/${getImageName(piece, color)}.png`}
                className="promote-piece"
                onClick={() => handlePromotion(from, to, piece)}
              />
            </div>
          </UISquare>
        </div>
      ))}
    </div>
  );
};

export default UIPromotion;
