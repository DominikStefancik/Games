import { PieceSymbol, Color } from 'chess.js/src/chess';
import { getImageName } from '@local/components/ui/board/helpers';

interface UIPieceProps {
  piece: PieceSymbol;
  color: Color;
}

const UIPiece = ({ piece, color }: UIPieceProps) => {
  const image = `./src/assets/${getImageName(piece, color)}`;

  return (
    <div className="piece-container">
      <img className="piece" src={image} />
    </div>
  );
};

export default UIPiece;
