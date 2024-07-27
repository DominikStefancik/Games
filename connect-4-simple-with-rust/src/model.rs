pub const BOARD_WIDTH: usize = 7;
pub const BOARD_HEIGHT: usize = 6;

pub type Board = [[u8; BOARD_WIDTH]; BOARD_HEIGHT];

pub const RESET_COLOR: &str = "\x1b[0m";
pub const ORANGE_COLOR: &str = "\x1b[93m";
pub const RED_COLOR: &str = "\x1b[0;31m";

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
            1 => Player::One,
            2 => Player::Two,
            _ => Player::None,
        }
    }
}
