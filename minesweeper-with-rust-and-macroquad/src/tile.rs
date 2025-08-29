use crate::assets::Assets;
use macroquad::color::{
    BLUE, BROWN, Color, DARKBLUE, GREEN, LIGHTGRAY, PINK, PURPLE, RED, SKYBLUE, WHITE,
};
use macroquad::math::Vec2;
use macroquad::shapes::draw_rectangle;
use macroquad::text::draw_text;
use macroquad::texture::{DrawTextureParams, draw_texture_ex};

#[derive(Clone, Debug, Eq, PartialEq)]
pub enum TileState {
    Hidden,
    Revealed,
    Flagged,
}

#[derive(Clone, Debug)]
pub struct Tile {
    pub state: TileState,
    pub contains_mine: bool,
    pub number_of_surrounding_mines: u32,
}

impl Tile {
    pub fn new() -> Self {
        Tile {
            state: TileState::Hidden,
            contains_mine: false,
            number_of_surrounding_mines: 0,
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

        if self.number_of_surrounding_mines > 0
            && self.state == TileState::Revealed
            && !self.contains_mine
        {
            let text_x = x_coordinate + tile_size / 2. - tile_size / 5.;
            let text_y = y_coordinate + tile_size / 2. + tile_size / 5.;

            draw_text(
                self.number_of_surrounding_mines.to_string().as_str(),
                text_x,
                text_y,
                tile_size,
                get_number_color(self.number_of_surrounding_mines),
            );
        }
    }

    pub fn reveal(&mut self) {
        self.state = TileState::Revealed;
    }

    pub fn flag(&mut self) {
        self.state = TileState::Flagged;
    }
}

fn get_number_color(number: u32) -> Color {
    match number {
        1 => BLUE,
        2 => GREEN,
        3 => RED,
        4 => DARKBLUE,
        5 => PINK,
        6 => SKYBLUE,
        7 => PURPLE,
        8 => BROWN,
        _ => WHITE,
    }
}
