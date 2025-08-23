#[derive(Clone, Debug)]
pub struct Tile {
    pub contains_mine: bool,
}

impl Tile {
    pub fn new() -> Self {
        Tile {
            contains_mine: false,
        }
    }
}