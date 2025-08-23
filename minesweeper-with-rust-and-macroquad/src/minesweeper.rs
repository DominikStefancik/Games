use crate::constants::{LEFT_MARGIN, TILE_SIZE, TOP_MARGIN};
use crate::tile::Tile;
use rand::Rng;

enum GameState {
    Playing,
    Won,
    Lost,
}

pub struct Minesweeper {
    pub rows: u32,
    pub cols: u32,
    pub tiles: Vec<Tile>,
    pub state: GameState,
}

impl Minesweeper {
    pub fn new(rows: u32, cols: u32, mines_count: u32) -> Self {
        let tiles = create_tiles(rows, cols, mines_count);

        Minesweeper {
            rows,
            cols,
            tiles,
            state: GameState::Playing,
        }
    }

    pub fn draw(&self) {
        for i in 0..self.rows {
            for j in 0..self.cols {
                let tile_index = self.get_index(i, j);
                let tile = &self.tiles[tile_index];
                tile.draw(
                    LEFT_MARGIN + i as f32 * TILE_SIZE,
                    TOP_MARGIN + j as f32 * TILE_SIZE,
                )
            }
        }
    }

    fn get_index(&self, row_index: u32, col_index: u32) -> usize {
        (self.cols * col_index + row_index) as usize
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
