use bevy::state::state::States;

#[derive(States, Debug, Clone, Copy, Eq, PartialEq, Hash, Default)]
pub enum GameState {
    // this says Running will be a default state of the game
    #[default]
    Playing,
    Paused,
    GameOver,
}
