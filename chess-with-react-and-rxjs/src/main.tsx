import React from 'react';
import ReactDOM from 'react-dom/client';
import ChessGame from '@local/root/ChessGame';
import './index.css';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <DndProvider backend={HTML5Backend}>
      <ChessGame />
    </DndProvider>
  </React.StrictMode>
);
