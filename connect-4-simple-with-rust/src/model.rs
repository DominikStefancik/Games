const BOARD_WIDTH: usize = 7;
const BOARD_HEIGHT: usize = 6;

type Board = [[u8; BOARD_WIDTH]; BOARD_HEIGHT];

#[derive(Clone, Copy, Debug, PartialEq)]
#[repr(u8)]
pub enum Player {
    One = 1,
    Two = 2,
    // this options is to present a value for non-winner, if the game ends in a draw
    None = 0,
}

impl From<u8> for Player {
    fn from(value: u8) -> Self {
        match value {
            0 => Player::None,
            1 => Player::One,
            2 => Player::Two,
            _ => Player::None,
        }
    }
}

pub struct Game {
    current_move: u8,
    current_player: Player,
    board: Board,
    is_finished: bool,
    winner: Player,
}

impl Game {
    pub fn default() -> Self {
        Game {
            current_move: 0,
            current_player: Player::One,
            board: [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
            is_finished: false,
            winner: Player::None,
        }
    }
}
