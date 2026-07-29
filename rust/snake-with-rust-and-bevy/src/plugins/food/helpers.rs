use crate::plugins::{
    food::{Food, FoodSprite},
    shared::{CELL_PADDING, FOOD_COLOR, Grid, GridPosition, Randomizer},
    snake::Snake,
};
use bevy::{ecs::system::Commands, math::Vec2, sprite::Sprite, transform::components::Transform};
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

pub fn render_food(commands: &mut Commands, grid: &Grid, food: &Food) {
    commands.spawn((
        Sprite::from_color(FOOD_COLOR, Vec2::splat((grid.pixels - CELL_PADDING) as f32)),
        Transform::from_translation(grid.to_pixels(food.0, 1.)),
        FoodSprite,
    ));
}
