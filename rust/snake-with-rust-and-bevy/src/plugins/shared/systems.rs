use bevy::{
    ecs::system::{Commands, Res, ResMut},
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State},
};

use crate::plugins::shared::{GameStarted, GameState};

pub fn initialise_game(mut commands: Commands) {
    commands.trigger(GameStarted);
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
            GameState::GameOver => {}
        }
    }
}
