use crate::{
    core::{Grid, GridPosition, Randomizer},
    plugins::snake::Snake,
};
use rand::RngExt;

fn random_food_position(randomizer: &mut Randomizer, grid: &Grid) -> GridPosition {
    let column = randomizer.rng.random_range(0..grid.size.x);
    let row = randomizer.rng.random_range(0..grid.size.y);

    GridPosition::new(column, row)
}

pub fn new_food_position(randomizer: &mut Randomizer, grid: &Grid, snake: &Snake) -> GridPosition {
    loop {
        let food_position = random_food_position(randomizer, grid);

        if !snake.segments.contains(&food_position) {
            return food_position;
        }
    }
}
