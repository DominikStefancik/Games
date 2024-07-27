use model::Game;

mod model;

fn main() {
    let mut game = Game::default();

    game.display_board();
}
