use crate::constants::TILE_SIZE;
use macroquad::color::SKYBLUE;
use macroquad::shapes::draw_rectangle;

#[derive(Clone, Debug)]
enum TileState {
    Hidden,
    Revealed,
    Flagged,
}

#[derive(Clone, Debug)]
pub struct Tile {
    pub state: TileState,
    pub contains_mine: bool,
}

impl Tile {
    pub fn new() -> Self {
        Tile {
            state: TileState::Hidden,
            contains_mine: false,
        }
    }

    pub fn draw(&self, x_coordinate: f32, y_coordinate: f32) {
        draw_rectangle(
            x_coordinate,
            y_coordinate,
            TILE_SIZE - 1.,
            TILE_SIZE - 1.,
            SKYBLUE,
        );
    }
}
