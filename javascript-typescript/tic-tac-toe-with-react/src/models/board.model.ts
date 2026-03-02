import { SquareType } from "./square.model";

export type BoardState = SquareType[];

// the type "history" will represent states of the board for each move
export type HistoryType = BoardState[];
