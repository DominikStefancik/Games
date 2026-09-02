use bevy::state::state::States;

#[derive(States, Debug, Clone, Copy, Eq, PartialEq, Hash, Default)]
pub enum GameState {
    // this says GameStarting will be a default state of the game
    #[default]
    GameStarting,
    Running,
    Paused,
    GameWin,
    GameOver,
}

pub fn is_game_starting_or_running(game_state: &GameState) -> bool {
    [GameState::GameStarting, GameState::Running].contains(game_state)
}
