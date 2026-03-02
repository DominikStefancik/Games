import { PieceSymbol, Color } from 'chess.js/src/chess';
import { getImageName } from '@local/components/ui/board/helpers';
import { useDrag, DragPreviewImage } from 'react-dnd';
import { DraggablePiece, DRAGGABLE_ITEM } from '@local/components/ui/board/models';

interface UIPieceProps {
  piece: PieceSymbol;
  color: Color;
  piecePosition: string;
}

const UIPiece = ({ piece, color, piecePosition }: UIPieceProps) => {
  const imageName = getImageName(piece, color);
  const [{ opacity }, dragReference, previewReference] = useDrag({
    type: DRAGGABLE_ITEM,
    item: { id: imageName, currentPosition: piecePosition } as DraggablePiece,
    collect: (monitor) => {
      const isPieceDragging = monitor.isDragging();

      return {
        opacity: isPieceDragging ? 0 : 1,
      };
    },
  });
  const image = `./src/assets/${imageName}.png`;

  return (
    <>
      <div className="square">
        <DragPreviewImage connect={previewReference} src={image} />
      </div>

      <div className="piece-container" ref={dragReference} style={{ opacity }}>
        <img className="piece" src={image} />
      </div>
    </>
  );
};

export default UIPiece;
