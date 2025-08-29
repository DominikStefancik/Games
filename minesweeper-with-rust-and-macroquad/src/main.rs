use crate::board::Board;
use crate::minesweeper::Minesweeper;
use macroquad::color::WHITE;
use macroquad::window::{clear_background, next_frame};

mod assets;
mod board;
mod constants;
mod minesweeper;
mod mouse;
mod position;
mod tile;

#[macroquad::main("Minesweeper with Macroquad")]
async fn main() {
    let mut game = Minesweeper::new(Board::small()).await;

    loop {
        clear_background(WHITE);

        game.handle_mouse_click();
        game.draw();

        next_frame().await;
    }
}
