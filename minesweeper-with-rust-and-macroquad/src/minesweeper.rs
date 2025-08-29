use crate::assets::Assets;
use crate::constants::{
    BOTTOM_MARGIN, LEFT_MARGIN, NEIGHBOURS_DIFFERENCE, RIGHT_MARGIN, TOP_MARGIN,
};
use crate::mouse::get_pressed_mouse_position;
use crate::position::Position;
use crate::tile::{Tile, TileState};
use macroquad::input::MouseButton;
use macroquad::window::{screen_height, screen_width};
use rand::Rng;
use std::collections::VecDeque;

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

        let mut game = Minesweeper {
            rows,
            cols,
            tiles,
            state: GameState::Playing,
            assets,
        };
        game.update_number_of_surrounding_mines();

        game
    }

    fn update_number_of_surrounding_mines(&mut self) {
        for i in 0..self.cols {
            for j in 0..self.rows {
                let position = Position::new(i as i32, j as i32);
                let tile_index = self.get_tile_index(&position);
                self.tiles[tile_index].number_of_surrounding_mines =
                    self.get_surrounding_mines_count(&position);
            }
        }
    }

    fn get_surrounding_mines_count(&self, tile_position: &Position<i32>) -> u32 {
        NEIGHBOURS_DIFFERENCE
            .iter()
            .map(|difference| tile_position.add(difference))
            .filter(|position| {
                self.is_within_board_bounds(position)
                    && self.tiles[self.get_tile_index(position)].contains_mine
            })
            .count() as u32
    }

    pub fn draw(&self) {
        let tile_size = self.get_tile_size();
        for i in 0..self.cols {
            for j in 0..self.rows {
                let tile_index = self.get_tile_index(&Position::new(i as i32, j as i32));
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

    fn get_tile_index(&self, position: &Position<i32>) -> usize {
        (self.cols * position.x as u32 + position.y as u32) as usize
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
            self.flag_tile(position)
        }
    }

    fn make_move(&mut self, position: Position<f32>) {
        // first find out which tile was clicked on via a cursor position
        let position = match self.resolve_tile_position(&position) {
            Some(position) => position,
            None => return,
        };

        // if the position is the position of a tile, we want to get the index of the tile
        let index = self.get_tile_index(&position);
        let tile = &mut self.tiles[index];

        match tile.state {
            TileState::Hidden if tile.contains_mine => {
                tile.reveal();
                println!("User clicked a mine. Game over!");
                self.state = GameState::Lost;
            }
            TileState::Hidden if !tile.contains_mine => {
                tile.reveal();
                self.reveal_neighbour_tiles(&position);
            }
            TileState::Revealed => {
                self.reveal_neighbour_tiles(&position);
            }
            _ => {}
        }
    }

    fn flag_tile(&mut self, position: Position<f32>) {
        // first find out which tile was clicked on via a cursor position
        let position = match self.resolve_tile_position(&position) {
            Some(position) => position,
            None => return,
        };

        // if the position is the position of a tile, we want to get the index of the tile
        let index = self.get_tile_index(&position);
        let tile = &mut self.tiles[index];
        tile.flag();
    }

    fn resolve_tile_position(&self, position: &Position<f32>) -> Option<Position<i32>> {
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

        // only if a cursor is in the board area, return a position
        if self.is_within_board_bounds(&result) {
            return Some(result);
        }

        None
    }

    fn is_within_board_bounds(&self, position: &Position<i32>) -> bool {
        position.x >= 0
            && position.y >= 0
            && position.x < self.cols as i32
            && position.y < self.rows as i32
    }

    // the method uses the Breadth First Search algorithm to reveal tiles
    // it starts with a tile on a board and investigates all tiles on the current depth level before moving
    // to the tiles on the next depth level
    fn reveal_neighbour_tiles(&mut self, position: &Position<i32>) {
        let mut queue: VecDeque<Position<i32>> = VecDeque::new();
        // we start with a tile a user clicked
        queue.push_back(position.clone());

        // then go over all surrounding tiles
        while let Some(position) = queue.pop_front() {
            for difference in NEIGHBOURS_DIFFERENCE {
                // for each neighbour we get a new position by adding the current position to the neighbour difference
                let neighbour_position = position.add(difference);

                // if a tile is on a border and adding a difference will take us out of the board
                if !self.is_within_board_bounds(&neighbour_position) {
                    continue;
                }

                let neighbour_tile_index = self.get_tile_index(&neighbour_position);
                let neighbour_tile = &mut self.tiles[neighbour_tile_index];

                if neighbour_tile.contains_mine || neighbour_tile.state != TileState::Hidden {
                    continue;
                }

                neighbour_tile.reveal();

                if neighbour_tile.number_of_surrounding_mines == 0 {
                    queue.push_back(neighbour_position);
                }
            }
        }
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
