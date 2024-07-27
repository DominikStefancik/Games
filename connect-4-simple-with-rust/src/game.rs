use crate::{
    constants::{Board, BOARD_HEIGHT, BOARD_WIDTH, ORANGE_COLOR, RED_COLOR, RESET_COLOR},
    move_error::MoveError,
    player::Player,
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

    pub fn is_finished(&self) -> bool {
        self.is_finished
    }

    pub fn current_player(&self) -> Player {
        self.current_player
    }

    pub fn display_board(&self) {
        // clears the screen
        print!("{}[2J", 27 as char);

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

    pub fn display_error(&self, error: String) {
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

            let calculated_winner = self.calculate_winner();

            if calculated_winner != Player::None {
                self.winner = calculated_winner;
            } else {
                self.current_player = match self.current_player {
                    Player::One => Player::Two,
                    Player::Two | Player::None => Player::One,
                }
            }
        } else {
            return Err(MoveError::ColumnFull);
        }

        Ok(())
    }

    fn calculate_winner(&mut self) -> Player {
        // if there are not enough moves to decide who the winner is
        if self.current_move < 7 {
            return Player::None;
        }

        // represent possible directions a winning line can have
        let directions = [
            (0, 1),  // horizontal line, we update y-axis
            (1, 0),  // vertical line, we update x-axis
            (1, 1),  // diagonal (top-left to bottom-right), we update both axis
            (-1, 1), // diagonal (bottom-left to top-right), we update both axis
        ];

        for row in 0..BOARD_HEIGHT {
            for column in 0..BOARD_WIDTH {
                let cell = self.board[row][column];

                if cell != 0 {
                    for (row_step, column_step) in directions {
                        let mut consecutive_count: u8 = 1;
                        let mut row_count = row as isize + row_step;
                        let mut column_count = column as isize + column_step;

                        while row_count >= 0
                            && row_count < BOARD_HEIGHT as isize
                            && column_count >= 0
                            && column_count < BOARD_WIDTH as isize
                        {
                            if self.board[row_count as usize][column_count as usize] == cell {
                                consecutive_count += 1;

                                if consecutive_count == 4 {
                                    self.is_finished = true;
                                    return Player::from(cell);
                                }
                            } else {
                                break;
                            }
                            row_count += row_step;
                            column_count += column_count;
                        }
                    }
                }
            }
        }

        // we reached that the whole board if full, but there is no winning line
        if self.current_move >= BOARD_HEIGHT as u8 * BOARD_WIDTH as u8 {
            self.is_finished = true;
        }

        Player::None
    }
}
