use bevy::{
    ecs::system::{Res, ResMut},
    state::state::{NextState, State, States},
    time::Time,
};

use crate::core::GameStartingTimer;

#[derive(States, Debug, Clone, Copy, Eq, PartialEq, Hash, Default)]
pub enum GameState {
    // this says Running will be a default state of the game
    #[default]
    GameStarting,
    Playing,
    Paused,
    GameOver,
}

pub fn move_to_playing_state(
    time: Res<Time>,
    mut timer: ResMut<GameStartingTimer>,
    app_state: Res<State<GameState>>,
    mut next_state: ResMut<NextState<GameState>>,
) {
    timer.0.tick(time.delta());

    let allowed_states = [GameState::GameStarting, GameState::GameOver];

    if timer.0.is_finished() && allowed_states.contains(app_state.get()) {
        next_state.set(GameState::Playing);
    }
}
