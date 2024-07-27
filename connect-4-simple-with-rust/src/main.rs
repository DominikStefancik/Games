use game::Game;

mod constants;
mod game;
mod move_error;
mod player;

fn main() {
    let mut game = Game::default();

    game.display_board();
}
