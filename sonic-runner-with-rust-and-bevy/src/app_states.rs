use bevy::{
    ecs::system::{Res, ResMut, Single},
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State, States},
};

use crate::entities::sonic::components::Sonic;

#[derive(States, Debug, Clone, Copy, Eq, PartialEq, Hash, Default)]
pub enum AppState {
    // this says MainMenu will be a default state of the app when we start it
    #[default]
    MainMenu,
    Game,
    GameOver,
}

pub fn move_to_game_state(
    keyboard_input: Res<ButtonInput<KeyCode>>,
    app_state: Res<State<AppState>>,
    mut next_state: ResMut<NextState<AppState>>,
) {
    if *app_state.get() != AppState::Game && keyboard_input.just_pressed(KeyCode::Space) {
        next_state.set(AppState::Game);
    }
}

pub fn move_to_game_over_state(
    app_state: Res<State<AppState>>,
    mut next_state: ResMut<NextState<AppState>>,
    sonic: Single<&Sonic>,
) {
    if *app_state.get() == AppState::Game && sonic.is_dead {
        next_state.set(AppState::GameOver);
    }
}
