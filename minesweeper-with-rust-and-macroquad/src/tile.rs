use crate::assets::Assets;
use macroquad::color::{LIGHTGRAY, SKYBLUE, WHITE};
use macroquad::math::Vec2;
use macroquad::shapes::draw_rectangle;
use macroquad::texture::{DrawTextureParams, draw_texture_ex};

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

    pub fn draw(&self, x_coordinate: f32, y_coordinate: f32, tile_size: f32, assets: &Assets) {
        let color = match self.state {
            TileState::Hidden | TileState::Flagged => SKYBLUE,
            TileState::Revealed => LIGHTGRAY,
        };
        draw_rectangle(
            x_coordinate,
            y_coordinate,
            tile_size - 1.,
            tile_size - 1.,
            color,
        );

        if let Some(asset) = match self.state {
            TileState::Flagged => Some(&assets.flag),
            TileState::Revealed if self.contains_mine => Some(&assets.mine),
            _ => None,
        } {
            draw_texture_ex(
                asset,
                x_coordinate,
                y_coordinate,
                WHITE,
                DrawTextureParams {
                    dest_size: Some(Vec2::splat(tile_size - 1.)),
                    ..Default::default()
                },
            );
        }
    }

    pub fn reveal(&mut self) {
        self.state = TileState::Revealed;
    }
}
