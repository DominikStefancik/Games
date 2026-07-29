use bevy::{
    ecs::system::{Commands, Res, ResMut},
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State},
};

use crate::plugins::{
    game::{GameRestarted, GameState},
    shared::{Direction, DirectionQueue},
    snake::Snake,
};

pub fn enqueue_snake_direction_on_keypress(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    mut queue: ResMut<DirectionQueue>,
    snake: Res<Snake>,
) {
    let arrow_keys = [
        KeyCode::ArrowLeft,
        KeyCode::ArrowRight,
        KeyCode::ArrowUp,
        KeyCode::ArrowDown,
    ];

    for key in arrow_keys
        .iter()
        .filter(|key| keyboard_input.just_pressed(**key))
    {
        if let Some(direction) = Direction::from_key(key)
            && !snake.direction.is_opposite(&direction)
        {
            queue.0.push_back(direction);
        };
    }
}

pub fn toggle_pausing_game_on_keypress(
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

pub fn reset_game_on_keypress(mut commands: Commands, keyboard_input: Res<ButtonInput<KeyCode>>) {
    if keyboard_input.just_pressed(KeyCode::Enter) {
        commands.trigger(GameRestarted);
    }
}
