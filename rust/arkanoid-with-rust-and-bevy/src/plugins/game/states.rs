use bevy::state::state::States;

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
