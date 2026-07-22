use bevy::ecs::{
    entity::{ContainsEntity, Entity},
    observer::On,
    query::With,
    system::{Commands, Res, ResMut, Single},
};

use crate::{
    core::{Grid, Randomizer},
    plugins::{
        food::{Food, FoodSprite, new_food_position, render_food},
        shared::{FoodConsumed, GameStarted},
        snake::Snake,
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

    render_food(&mut commands, &grid, &food);
}

pub fn create_new_food(
    _: On<FoodConsumed>,
    mut commands: Commands,
    randomizer: ResMut<Randomizer>,
    grid: Res<Grid>,
    snake: ResMut<Snake>,
    mut food: ResMut<Food>,
    food_sprite: Single<Entity, With<FoodSprite>>,
) {
    let position = new_food_position(randomizer.into_inner(), &grid, &snake);
    food.0 = position;

    commands.entity(food_sprite.entity()).despawn();
    render_food(&mut commands, &grid, &food);
}
