use rand::Rng;
use crate::tile::Tile;

enum GameState {
    Playing,
    Won,
    Lost
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
