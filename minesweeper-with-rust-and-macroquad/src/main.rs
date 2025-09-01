use crate::board::Board;
use crate::controls::{Controls, RectangleType};
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

#[macroquad::main("Rust Minesweeper")]
async fn main() {
    let mut game = Minesweeper::new(Board::small()).await;
    let controls = Controls::new();

    loop {
        clear_background(WHITE);

        controls.draw();
        controls.show_finishing_text(&game.state);

        let click_result = controls.handle_mouse_click();

        if let Some(rectangle) = click_result {
            let board = match rectangle.rectangle_type {
                RectangleType::Small => Board::small(),
                RectangleType::Medium => Board::medium(),
                RectangleType::Large => Board::large(),
            };
            game = Minesweeper::new(board).await;
        }

        game.handle_mouse_click();
        game.draw();

        next_frame().await;
    }
}
