use crate::{
    model::{Board, Player, BOARD_HEIGHT, BOARD_WIDTH, ORANGE_COLOR, RED_COLOR, RESET_COLOR},
    move_error::MoveError,
};

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
            current_move: 0, // track the number of moves
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
        println!("{}--------------------{}", ORANGE_COLOR, RESET_COLOR);
        println!(
            "{}Connect 4 (Move {}){}",
            ORANGE_COLOR, self.current_move, RESET_COLOR
        );
        println!("{}--------------------{}", ORANGE_COLOR, RESET_COLOR);

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

        println!("{}--------------------{}", ORANGE_COLOR, RESET_COLOR);

        if self.is_finished {
            match self.winner {
                Player::One => println!("{}🔴 Player 1 has won!{}", ORANGE_COLOR, RESET_COLOR),
                Player::Two => println!("{}🟡 Player 2 has won!{}", ORANGE_COLOR, RESET_COLOR),
                Player::None => println!("{}It's a draw!{}", ORANGE_COLOR, RESET_COLOR),
            }
        }

        println!("{}--------------------{}", ORANGE_COLOR, RESET_COLOR);
    }

    pub fn display_error(&self, error: MoveError) {
        self.display_board();
        println!("{}Error: {}{}", RED_COLOR, error, RESET_COLOR);
    }

    pub fn play_move(&mut self, column: usize) -> Result<(), MoveError> {
        if self.is_finished {
            return Err(MoveError::GameFinished);
        }

        if column >= BOARD_WIDTH {
            return Err(MoveError::InvalidColumn);
        }

        // go from the bottom up and find the first row which contains at least one zero
        // in that row we find the first column which has zero
        if let Some(row) = (0..BOARD_HEIGHT)
            .rev()
            .find(|&row| self.board[row][column] == 0)
        {
            self.board[row][column] = self.current_player as u8;
            self.current_move += 1;

            self.current_player = match self.current_player {
                Player::One => Player::Two,
                Player::Two | Player::None => Player::One,
            }
        } else {
            return Err(MoveError::ColumnFull);
        }

        Ok(())
    }
}
