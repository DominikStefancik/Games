use bevy::{
    ecs::system::ResMut,
    state::state::{NextState, States},
};

#[derive(States, Debug, Clone, Copy, Eq, PartialEq, Hash, Default)]
pub enum GameState {
    // this says Loading will be a default state of the game
    #[default]
    Loading,
    NewLevelStarting,
    BallReady,
    Running,
    Paused,
    GameWin,
    GameOver,
}

pub fn finish_loading(mut next_state: ResMut<NextState<GameState>>) {
    next_state.set(GameState::NewLevelStarting);
}

pub fn finish_level_start(mut next_state: ResMut<NextState<GameState>>) {
    next_state.set(GameState::BallReady);
}
