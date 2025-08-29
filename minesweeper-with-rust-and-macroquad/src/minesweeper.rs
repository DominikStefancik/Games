use crate::assets::Assets;
use crate::board::Board;
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

#[derive(PartialEq)]
pub enum GameState {
    Playing,
    Won,
    Lost,
}

pub struct Minesweeper {
    pub board: Board,
    pub tiles: Vec<Tile>,
    pub state: GameState,
    pub assets: Assets,
}

impl Minesweeper {
    pub async fn new(board: Board) -> Self {
        let tiles = create_tiles(&board);
        let assets = Assets::load().await;

        let mut game = Minesweeper {
            board,
            tiles,
            state: GameState::Playing,
            assets,
        };
        game.update_number_of_surrounding_mines();

        game
    }

    fn update_number_of_surrounding_mines(&mut self) {
        for i in 0..self.board.cols {
            for j in 0..self.board.rows {
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
        for i in 0..self.board.cols {
            for j in 0..self.board.rows {
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
        (self.board.cols * position.x as u32 + position.y as u32) as usize
    }

    /*
     * Calculates the size of a tile dynamically, depending on how the size of the window changes
     */
    fn get_tile_size(&self) -> f32 {
        let width = (screen_width() - LEFT_MARGIN - RIGHT_MARGIN) / self.board.cols as f32;
        let height = (screen_height() - TOP_MARGIN - BOTTOM_MARGIN) / self.board.rows as f32;

        width.min(height)
    }

    pub fn handle_mouse_click(&mut self) {
        // don't react to a user click if the game is over
        if self.state != GameState::Playing {
            return;
        }

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
                println!("You clicked on a mine. Game over!");
                self.state = GameState::Lost;
            }
            TileState::Hidden if !tile.contains_mine => {
                tile.reveal();
                self.reveal_neighbour_tiles(&position);
            }
            TileState::Revealed => {
                if self.can_reveal_neighbour_tiles(&position) {
                    self.reveal_neighbour_tiles(&position);
                }
            }
            _ => {}
        }

        if self.has_won() {
            println!("You won!");
            self.state = GameState::Won;
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

        // if user wants to flag an already revealed tile, we don't allow it
        if tile.state == TileState::Revealed {
            return;
        }

        tile.toggle_flag();
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
            && position.x < self.board.cols as i32
            && position.y < self.board.rows as i32
    }

    // the method uses the Breadth First Search algorithm to reveal tiles
    // it starts with a tile on a board and investigates all tiles on the current depth level before moving
    // to the tiles on the next depth level
    fn reveal_neighbour_tiles(&mut self, position: &Position<i32>) {
        let mut queue: VecDeque<Position<i32>> = VecDeque::new();
        // we start with a tile a user clicked
        queue.push_back(*position);

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

    fn can_reveal_neighbour_tiles(&self, position: &Position<i32>) -> bool {
        let index = self.get_tile_index(position);
        let tile = &self.tiles[index];

        // if this tile has no mines around it, then it has been already revealed
        // if it has a mine, the game is lost anyway
        if tile.number_of_surrounding_mines == 0 || tile.contains_mine {
            return false;
        }

        // check if the number of tiles a user flagged correctly equals the number of mines around this tile
        let count = NEIGHBOURS_DIFFERENCE
            .iter()
            .map(|difference| position.add(difference))
            .filter(|position| self.is_within_board_bounds(position))
            .map(|position| {
                let neighbour_index = self.get_tile_index(&position);
                let neighbour_tile = &self.tiles[neighbour_index];

                match (neighbour_tile.contains_mine, &neighbour_tile.state) {
                    (true, TileState::Flagged) => 1,
                    (false, TileState::Flagged) => 100000, // means a user flagged the tile incorrectly
                    _ => 0,
                }
            })
            .sum();

        tile.number_of_surrounding_mines == count
    }

    fn has_won(&self) -> bool {
        self.tiles
            .iter()
            .filter(|tile| !tile.contains_mine)
            .all(|tile| tile.state == TileState::Revealed)
    }
}

fn create_tiles(board: &Board) -> Vec<Tile> {
    let Board {
        rows,
        cols,
        mines_count,
    } = board;

    // it better to treat tiles as one-dimensional array rather than two-dimensional
    // because it will be faster and more efficient memory wise
    let mut tiles = vec![Tile::new(); (rows * cols) as usize];
    let mut rnd = rand::rng();

    (0..*mines_count).for_each(|_| {
        let mut index = rnd.random_range(0..(rows * cols) as usize);

        while tiles[index].contains_mine {
            index = rnd.random_range(0..(rows * cols) as usize);
        }

        tiles[index].contains_mine = true;
    });

    tiles
}
