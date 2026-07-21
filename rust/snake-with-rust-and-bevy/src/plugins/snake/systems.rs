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
    core::{CELL_PADDING, Grid, GridPosition, SNAKE_COLOR},
    plugins::{shared::GameStarted, snake::Snake},
};

pub fn setup_snake(mut commands: Commands, grid: Res<Grid>) {
    let start_column = grid.size.x / 2;
    let start_row = grid.size.y / 2;

    let snake = Snake::new(start_column, start_row);

    /*
     * Commands don't mutate the World immediately — they queue up a command, and that queue is only applied ("flushed")
     * at a sync point (an apply_deferred call Bevy inserts into the schedule graph).
     * So the resource doesn't exist in the World the instant that line runs; it exists once the next sync point is reached.
     *
     * When running World::insert_resource, this mutates the World immediately — no queue, no sync point needed.
     * Any system that runs after this one (in schedule order) will see it right away.
     */

    commands.insert_resource(snake);
}

pub fn initialise_snake(
    _: On<GameStarted>,
    mut commands: Commands,
    grid: Res<Grid>,
    mut snake: ResMut<Snake>,
) {
    let center_position = GridPosition::new(grid.size.x / 2, grid.size.y / 2);
    snake.restart(center_position.column, center_position.row);

    for segment in &snake.segments {
        commands.spawn((
            Sprite::from_color(
                SNAKE_COLOR,
                Vec2::splat((grid.pixels - CELL_PADDING) as f32),
            ),
            Transform::from_translation(grid.to_pixels(*segment, 1.)),
        ));
    }
}
