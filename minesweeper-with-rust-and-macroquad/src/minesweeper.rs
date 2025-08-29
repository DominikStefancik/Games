use crate::assets::Assets;
use crate::constants::{BOTTOM_MARGIN, LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN};
use crate::mouse::get_pressed_mouse_position;
use crate::position::Position;
use crate::tile::Tile;
use macroquad::input::MouseButton;
use macroquad::window::{screen_height, screen_width};
use rand::Rng;

pub enum GameState {
    Playing,
    Won,
    Lost,
}

pub struct Minesweeper {
    pub rows: u32,
    pub cols: u32,
    pub tiles: Vec<Tile>,
    pub state: GameState,
    pub assets: Assets,
}

impl Minesweeper {
    pub async fn new(rows: u32, cols: u32, mines_count: u32) -> Self {
        let tiles = create_tiles(rows, cols, mines_count);
        let assets = Assets::load().await;

        Minesweeper {
            rows,
            cols,
            tiles,
            state: GameState::Playing,
            assets,
        }
    }

    pub fn draw(&self) {
        let tile_size = self.get_tile_size();
        for i in 0..self.rows {
            for j in 0..self.cols {
                let tile_index = self.get_index(&Position::new(i, j));
                let tile = &self.tiles[tile_index];
                tile.draw(
                    LEFT_MARGIN + i as f32 * tile_size,
                    TOP_MARGIN + j as f32 * tile_size,
                    tile_size,
                    &self.assets,
                )
            }
        }
    }

    fn get_index(&self, position: &Position<u32>) -> usize {
        (self.cols * position.x + position.y) as usize
    }

    /*
     * Calculates the size of a tile dynamically, depending on how the size of the window changes
     */
    fn get_tile_size(&self) -> f32 {
        let width = (screen_width() - LEFT_MARGIN - RIGHT_MARGIN) / self.cols as f32;
        let height = (screen_height() - TOP_MARGIN - BOTTOM_MARGIN) / self.rows as f32;

        width.min(height)
    }

    pub fn handle_mouse_click(&mut self) {
        if let Some(position) = get_pressed_mouse_position(MouseButton::Left) {
            self.make_move(position);
        } else if let Some(position) = get_pressed_mouse_position(MouseButton::Right) {
        }
    }

    fn make_move(&mut self, position: Position<f32>) {
        // first find out which tile was clicked on via a cursor position
        let position = match self.resolve_tile_position(&position) {
            Some(position) => position,
            None => return,
        };

        // if the position is the position of a tile, we want to get the index of the tile
        let index = self.get_index(&position);
        let tile = &mut self.tiles[index];
        tile.reveal();
    }

    fn resolve_tile_position(&self, position: &Position<f32>) -> Option<Position<u32>> {
        let tile_size = self.get_tile_size();
        // we need to remove the padding in case a cursor is slightly away from a tile square, where the padding is
        let position_without_padding = position.subtract(&Position::new(LEFT_MARGIN, TOP_MARGIN));

        // since we subtract the margins, we need to check if any of the position value is below zero
        if position_without_padding.x < 0. || position_without_padding.y < 0. {
            return None;
        }

        // we need to divide by the tile size to pixel position down to tile position
        let divided_position = position_without_padding.divide(tile_size);
        let result = divided_position.into();

        // only if a cursor is "in" the tile area, return a position
        if self.is_within_bounds(&result) {
            return Some(result);
        }

        None
    }

    fn is_within_bounds(&self, position: &Position<u32>) -> bool {
        // since the Position type can have only positive values, we can skip the test for
        // position.x >= 0 && position.y >= 0
        position.x < self.cols && position.y < self.rows
    }
}

fn create_tiles(rows: u32, cols: u32, mines_count: u32) -> Vec<Tile> {
    // it better to treat tiles as one-dimensional array rather than two-dimensional
    // because it will be faster and more efficient memory wise
    let mut tiles = vec![Tile::new(); (rows * cols) as usize];
    let mut rnd = rand::rng();

    (0..mines_count).for_each(|_| {
        let mut index = rnd.random_range(0..(rows * cols) as usize);

        while tiles[index].contains_mine {
            index = rnd.random_range(0..(rows * cols) as usize);
        }

        tiles[index].contains_mine = true;
    });

    tiles
}
