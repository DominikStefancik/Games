use bevy::{
    ecs::{
        observer::On,
        system::{Commands, Res, ResMut},
    },
    math::Vec2,
    sprite::Sprite,
    transform::components::Transform,
};

use crate::{
    core::{CELL_PADDING, FOOD_COLOR, Grid, Randomizer},
    plugins::{
        food::{helpers::new_food_position, resources::Food},
        shared::events::GameStarted,
        snake::resources::Snake,
    },
};

pub fn setup_food(mut commands: Commands, grid: Res<Grid>) {
    let start_column = grid.size.x / 2;
    let start_row = grid.size.y / 2;

    let food = Food::new(start_column, start_row);

    commands.insert_resource(food);
}

pub fn initialise_food(
    _: On<GameStarted>,
    mut commands: Commands,
    randomizer: ResMut<Randomizer>,
    grid: Res<Grid>,
    snake: ResMut<Snake>,
    mut food: ResMut<Food>,
) {
    let position = new_food_position(randomizer.into_inner(), &grid, &snake);
    food.0 = position;

    commands.spawn((
        Sprite::from_color(FOOD_COLOR, Vec2::splat((grid.pixels - CELL_PADDING) as f32)),
        Transform::from_translation(grid.to_pixels(food.0, 1.)),
    ));
}
