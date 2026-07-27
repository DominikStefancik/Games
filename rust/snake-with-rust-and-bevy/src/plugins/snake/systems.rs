use bevy::{
    audio::{AudioPlayer, PlaybackSettings, Volume},
    ecs::{
        entity::Entity,
        observer::On,
        query::With,
        system::{Commands, Query, Res, ResMut},
    },
    state::state::NextState,
    time::Time,
};

use crate::{
    core::{Direction, DirectionQueue, GameSounds, Grid, GridPosition, MoveTimer},
    plugins::{
        food::Food,
        shared::{FoodConsumed, GameStartTriggered, GameState},
        snake::{Snake, components::SnakeSegmentSprite, render_snake},
    },
};

pub fn initialise_snake(
    _: On<GameStartTriggered>,
    mut commands: Commands,
    grid: Res<Grid>,
    mut snake: ResMut<Snake>,
) {
    let center_position = GridPosition::new(grid.size.x / 2, grid.size.y / 2);
    snake.restart(center_position.column, center_position.row);
    render_snake(&mut commands, &grid, &snake);
}

#[allow(clippy::too_many_arguments)]
pub fn move_snake(
    mut commands: Commands,
    time: Res<Time>,
    mut timer: ResMut<MoveTimer>,
    mut next_state: ResMut<NextState<GameState>>,
    grid: Res<Grid>,
    game_sounds: Res<GameSounds>,
    mut queue: ResMut<DirectionQueue>,
    mut snake: ResMut<Snake>,
    snake_segments: Query<Entity, With<SnakeSegmentSprite>>,
    food: Res<Food>,
) {
    // Advance the timer.
    timer.0.tick(time.delta());

    // Continue only if the timer finished an interval
    if !timer.0.just_finished() {
        return;
    }

    while let Some(next_direction) = queue.0.pop_front() {
        if !snake.direction.is_opposite(&next_direction) {
            snake.direction = next_direction;
        }
    }

    let head = snake.segments[0];
    let new_head_position = match snake.direction {
        Direction::Left => GridPosition::new(head.column - 1, head.row),
        Direction::Right => GridPosition::new(head.column + 1, head.row),
        Direction::Up => GridPosition::new(head.column, head.row + 1),
        Direction::Down => GridPosition::new(head.column, head.row - 1),
    };

    if new_head_position.column < 0
        || new_head_position.column == grid.size.y
        || new_head_position.row < 0
        || new_head_position.row == grid.size.x
    {
        commands.spawn((
            AudioPlayer::new(game_sounds.die.clone()),
            PlaybackSettings::DESPAWN.with_volume(Volume::Linear(0.5)),
        ));
        next_state.set(GameState::GameOver);
        return;
    }

    if snake.segments.contains(&new_head_position) {
        commands.spawn((
            AudioPlayer::new(game_sounds.die.clone()),
            PlaybackSettings::DESPAWN.with_volume(Volume::Linear(0.5)),
        ));
        next_state.set(GameState::GameOver);
        return;
    }

    snake.segments.insert(0, new_head_position);

    if new_head_position == food.0 {
        commands.spawn((
            AudioPlayer::new(game_sounds.eat.clone()),
            PlaybackSettings::DESPAWN.with_volume(Volume::Linear(0.5)),
        ));
        commands.trigger(FoodConsumed);
    } else {
        snake.segments.pop();
    }

    // First remove the snake visually from the old position
    for sprite in snake_segments {
        commands.entity(sprite).despawn();
    }
    // And then re-render it
    render_snake(&mut commands, &grid, &snake);
}
