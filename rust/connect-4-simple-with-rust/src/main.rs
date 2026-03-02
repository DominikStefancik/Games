use game::Game;
use player::Player;
use std::io;

mod constants;
mod game;
mod move_error;
mod player;

fn main() {
    let mut game = Game::default();

    game.display_board();

    loop {
        play_game(&mut game);

        println!("Press 'R' to restart or 'Q' to quit the game");

        let mut user_input = String::new();

        io::stdin()
            .read_line(&mut user_input)
            .expect("Failed to read user's input");

        match user_input.trim() {
            "R" | "r" => {
                game = Game::default();
                continue;
            }
            "Q" | "q" => {
                println!("Quitting the game...");
                break;
            }
            _ => {
                game.display_error("Invalid input".to_string());
            }
        }
    }
}

fn play_game(game: &mut Game) {
    while !game.is_finished() {
        println!("\n");

        match game.current_player() {
            Player::One => println!("PLAYER 1"),
            Player::Two => println!("PLAYER 2"),
            _ => (),
        }

        println!("Enter a column between 1 and 7:");

        let mut user_move = String::new();
        io::stdin()
            .read_line(&mut user_move)
            .expect("Failed to read user's input");

        let user_move: usize = match user_move.trim().parse() {
            Ok(number) => {
                if !(1..=7).contains(&number) {
                    game.display_error(move_error::MoveError::InvalidColumn.to_string());
                    continue;
                } else {
                    number
                }
            }
            Err(error) => {
                game.display_error(error.to_string());
                continue;
            }
        };

        match game.play_move(user_move - 1) {
            Ok(_) => game.display_board(),
            Err(error) => game.display_error(error.to_string()),
        };
    }
}
