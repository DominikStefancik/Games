const BOARD_WIDTH: usize = 7;
const BOARD_HEIGHT: usize = 6;

type Board = [[u8; BOARD_WIDTH]; BOARD_HEIGHT];

const RESET_COLOR: &str = "\x1b[0m";
const ORANGE_COLOR: &str = "\x1b[93m";
const RED_COLOR: &str = "\x1b[0;31m";

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

    pub fn display_board(&self) {
        println!("{}-------------------{}", ORANGE_COLOR, RESET_COLOR);
        println!(
            "{}Connect 4 (Move {}){}",
            ORANGE_COLOR, self.current_move, RESET_COLOR
        );
        println!("{}-------------------{}", ORANGE_COLOR, RESET_COLOR);

        for row in self.board {
            let row_string = row
                .iter()
                .map(|&cell| match cell {
                    1 => "🔴",
                    2 => "🟡",
                    _ => "⚫",
                })
                .collect::<Vec<&str>>()
                .join(" ");

            println!("{}", row_string);
        }

        println!("{}-------------------{}", ORANGE_COLOR, RESET_COLOR);

        if self.is_finished {
            match self.winner {
                Player::One => println!("{}🔴 Player 1 has won!{}", ORANGE_COLOR, RESET_COLOR),
                Player::Two => println!("{}🟡 Player 2 has won!{}", ORANGE_COLOR, RESET_COLOR),
                Player::None => println!("{}It's a draw!{}", ORANGE_COLOR, RESET_COLOR),
            }
        }

        println!("{}-------------------{}", ORANGE_COLOR, RESET_COLOR);
    }
}
