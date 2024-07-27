pub const BOARD_WIDTH: usize = 7;
pub const BOARD_HEIGHT: usize = 6;

pub type Board = [[u8; BOARD_WIDTH]; BOARD_HEIGHT];

pub const RESET_COLOR: &str = "\x1b[0m";
pub const ORANGE_COLOR: &str = "\x1b[93m";
pub const RED_COLOR: &str = "\x1b[0;31m";
