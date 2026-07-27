use bevy::{
    ecs::{
        entity::{ContainsEntity, Entity},
        observer::On,
        query::With,
        system::{Commands, Query, Res, ResMut, Single},
    },
    input::{ButtonInput, keyboard::KeyCode},
    sprite::Text2d,
    state::state::{NextState, State},
};

use crate::{
    core::{DirectionQueue, MoveTimer},
    plugins::{
        food::FoodSprite,
        score::{Score, ScoreTextUi},
        shared::{GameRestarted, GameStartTriggered, GameState},
        snake::SnakeSegmentSprite,
    },
};

pub fn trigger_game_start(mut commands: Commands) {
    commands.trigger(GameStartTriggered);
}

pub fn toggle_pausing_game(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    game_state: Res<State<GameState>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    if keyboard_input.just_pressed(KeyCode::Space) {
        match game_state.get() {
            GameState::Playing => {
                next_state.set(GameState::Paused);
            }
            GameState::Paused => {
                next_state.set(GameState::Playing);
            }
            _ => {}
        }
    }
}

#[allow(clippy::too_many_arguments)]
pub fn reset_game(
    _: On<GameRestarted>,
    mut commands: Commands,
    mut move_timer: ResMut<MoveTimer>,
    mut queue: ResMut<DirectionQueue>,
    snake_segments: Query<Entity, With<SnakeSegmentSprite>>,
    food: Single<Entity, With<FoodSprite>>,
    mut score: ResMut<Score>,
    mut text_query: Single<&mut Text2d, With<ScoreTextUi>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    for segment_entity in snake_segments {
        commands.entity(segment_entity).despawn();
    }

    commands.entity(food.entity()).despawn();

    score.current = 0;
    text_query.0 = score.current.to_string();

    queue.0.clear();
    move_timer.0.reset();

    // Only after all that needs to be reset, we can start the game again by setting the state
    // (which will then run the "trigger_game_start" system)
    next_state.set(GameState::GameStarting);
}
