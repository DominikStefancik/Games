use bevy::{
    ecs::system::{Res, ResMut},
    input::{ButtonInput, keyboard::KeyCode},
    state::state::{NextState, State, States},
};

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
) {
    let is_sonic_dead = false;
    if *app_state.get() == AppState::Game && is_sonic_dead {
        next_state.set(AppState::GameOver);
    }
}
