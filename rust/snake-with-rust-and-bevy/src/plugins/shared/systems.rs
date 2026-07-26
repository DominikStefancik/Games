use bevy::{
    ecs::system::{Commands, Res, ResMut},
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State},
};

use crate::plugins::shared::{GameStartTriggered, GameState};

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
