import React, { useEffect, useState } from 'react';
import './ChessGame.css';
import { gameSubject, initializeGame } from '@local/components/non-ui/GameEngine';
import UIBoard from '@local/components/ui/board';
import { BoardSquare } from '@local/components/non-ui/models';

function ChessGame() {
  const [board, setBoard] = useState<(BoardSquare | null)[][]>([]);
  // start subscription to game subject when the main game component is created
  useEffect(() => {
    initializeGame();
    const gameSubscription = gameSubject.subscribe((game) => setBoard(game.board));

    // this returned functions is called when the component is unmounted
    // when the component is unmounted, clean up the subscription
    return () => {
      gameSubscription.unsubscribe();
    };
  }, []);

  return (
    <>
      <div className="global-container">
        <div className="board-container">
          <UIBoard board={board} />
        </div>
      </div>
    </>
  );
}

export default ChessGame;
