use crate::board::Board;
use crate::controls::Controls;
use crate::minesweeper::Minesweeper;
use macroquad::color::WHITE;
use macroquad::window::{clear_background, next_frame};

mod assets;
mod board;
mod constants;
mod controls;
mod minesweeper;
mod mouse;
mod position;
mod tile;

#[macroquad::main("Minesweeper with Macroquad")]
async fn main() {
    let mut game = Minesweeper::new(Board::small()).await;
    let controls = Controls::new();

    loop {
        clear_background(WHITE);

        controls.draw();
        controls.handle_mouse_click();

        game.handle_mouse_click();
        game.draw();

        next_frame().await;
    }
}
