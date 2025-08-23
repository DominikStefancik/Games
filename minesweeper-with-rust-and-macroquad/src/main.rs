use macroquad::color::WHITE;
use macroquad::window::{clear_background, next_frame};
use crate::minesweeper::Minesweeper;

mod minesweeper;
mod tile;

#[macroquad::main("Minesweeper with Macroquad")]
async fn main() {
    let game = Minesweeper::new(10, 10, 10);
    loop {
        clear_background(WHITE);

        next_frame().await;
    }
}
