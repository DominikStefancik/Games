use game::Game;

mod game;
mod model;
mod move_error;

fn main() {
    let mut game = Game::default();

    game.display_board();
}
