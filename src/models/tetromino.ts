export interface Tetromino {
  shape: (number | string)[][];
  rgb_colour: string;
}

export const NoShape: Tetromino = {
  shape: [[0]],
  rgb_colour: "0, 0, 0",
};

const I_Shape: Tetromino = {
  shape: [
    [0, "I", 0, 0],
    [0, "I", 0, 0],
    [0, "I", 0, 0],
    [0, "I", 0, 0],
  ],
  rgb_colour: "80, 227, 230",
};

const J_Shape: Tetromino = {
  shape: [
    [0, "J", 0],
    [0, "J", 0],
    ["J", "J", 0],
  ],
  rgb_colour: "36, 95, 223",
};

const L_Shape: Tetromino = {
  shape: [
    [0, "L", 0],
    [0, "L", 0],
    [0, "L", "L"],
  ],
  rgb_colour: "223, 173, 36",
};

const O_Shape: Tetromino = {
  shape: [
    ["O", "O"],
    ["O", "O"],
  ],
  rgb_colour: "223, 217, 36",
};

const S_shape: Tetromino = {
  shape: [
    [0, "S", "S"],
    ["S", "S", 0],
    [0, 0, 0],
  ],
  rgb_colour: "48, 211, 56",
};

const T_Shape: Tetromino = {
  shape: [
    [0, 0, 0],
    ["T", "T", "T"],
    [0, "T", 0],
  ],
  rgb_colour: "123, 61, 198",
};

const Z_Shape: Tetromino = {
  shape: [
    ["Z", "Z", 0],
    [0, "Z", "Z"],
    [0, 0, 0],
  ],
  rgb_colour: "227, 78, 78",
};

export const TETROMINOS = [I_Shape, J_Shape, L_Shape, O_Shape, S_shape, T_Shape, Z_Shape];
