use bevy::{
    app::{App, Plugin, Startup, Update},
    ecs::schedule::IntoScheduleConfigs,
    state::{app::AppExtStates, condition::in_state, state::OnEnter},
};

mod components;
mod constants;
mod helpers;
mod levels;
mod resources;
mod states;
mod systems;

pub use components::*;
pub use constants::*;
pub use helpers::*;
pub use levels::*;
pub use resources::*;
pub use states::*;
pub use systems::*;

pub struct GamePlugin;

impl Plugin for GamePlugin {
    fn build(&self, app: &mut App) {
        app.init_state::<GameState>()
            .insert_resource(GameInfo::init())
            .insert_resource(MovingArea::new())
            .add_systems(OnEnter(GameState::GameWin), spawn_game_finished_text)
            .add_systems(OnEnter(GameState::GameOver), spawn_game_finished_text)
            .add_systems(
                Startup,
                (spawn_background, spawn_score_text, spawn_hearts).chain(),
            )
            .add_systems(
                Update,
                (
                    finish_level_start.run_if(in_state(GameState::NewLevelStarting)),
                    is_level_finished.run_if(in_state(GameState::Running)),
                ),
            )
            // Global observers
            .add_observer(spawn_new_heart)
            .add_observer(update_score)
            .add_observer(restart_gaming_state);
    }
}
